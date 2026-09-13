import asyncio
import base64
import hashlib
import json
import logging
import os
import re
import secrets
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import func, or_
from sqlmodel import Session, select

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from db import engine
from models import Investigation, SafetyRating, Tsb
from report_template import build_report_html, make_report_number
from cache import TTLCache

REPORT_CACHE = TTLCache(ttl_seconds=3600, max_items=5000)
LOOKUP_CACHE = TTLCache(ttl_seconds=86400, max_items=20000)
PDF_CACHE = TTLCache(ttl_seconds=3600, max_items=2000)
PENDING_ORDERS: dict[str, dict[str, Any]] = {}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vin-report")

def get_client_ip(request: Request) -> str:
    peer = request.client.host if request.client else ""
    xff = request.headers.get("x-forwarded-for")
    if xff and peer in ("127.0.0.1", "::1"):
        ips = [ip.strip() for ip in xff.split(",") if ip.strip()]
        if ips:
            return ips[-1]
    return peer or "unknown"


limiter = Limiter(
    key_func=get_client_ip,
    default_limits=["120/minute"],
    headers_enabled=False,
)

app = FastAPI(
    title="VIN Report API",
    description="Aggregates vehicle data from NHTSA and fueleconomy.gov for a VIN report.",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VPIC_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
RECALLS_URL = "https://api.nhtsa.gov/recalls/recallsByVehicle"
COMPLAINTS_URL = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
SAFETY_BY_MODEL_URL = "https://api.nhtsa.gov/SafetyRatings/modelyear/{year}/make/{make}/model/{model}?format=json"
SAFETY_VEHICLE_URL = "https://api.nhtsa.gov/SafetyRatings/VehicleId/{vehicle_id}?format=json"
EPA_OPTIONS_URL = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year={year}&make={make}&model={model}"
EPA_VEHICLE_URL = "https://www.fueleconomy.gov/ws/rest/vehicle/{vehicle_id}"
GLOBALVIN_CARFAX_URL = "{base}/api/usa/report/carfax/{vin}"
GLOBALVIN_AUTOCHECK_URL = "{base}/api/usa/report/autocheck/{vin}"
GLOBALVIN_CHECK_RECORDS_URL = "{base}/api/usa/checkrecords/{vin}"

TIMEOUT = httpx.Timeout(20.0)
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) VINReport/0.1 (+contact)"}

PHOTO_DIR = Path(__file__).resolve().parent / "data" / "photos"

try:
    from pypdf import PdfReader, PdfWriter

    PDF_PROTECTION_AVAILABLE = True
except ImportError:  # pragma: no cover
    PDF_PROTECTION_AVAILABLE = False

QBO_CREDENTIALS_FILE = Path(__file__).resolve().parent / "data" / "qbo_credentials.json"


def _load_qb_credentials() -> dict[str, str]:
    try:
        data = json.loads(QBO_CREDENTIALS_FILE.read_text(encoding="utf-8"))
        return {k: str(v) for k, v in data.items() if isinstance(v, str) and v}
    except FileNotFoundError:
        return {}
    except Exception as exc:
        logger.warning("Could not read %s: %s", QBO_CREDENTIALS_FILE, exc)
        return {}


def _save_qb_credentials(**updates: str | None) -> None:
    data = _load_qb_credentials()
    for key, value in updates.items():
        if value:
            data[key] = value
        else:
            data.pop(key, None)
    try:
        QBO_CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        QBO_CREDENTIALS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        os.chmod(QBO_CREDENTIALS_FILE, 0o600)
    except Exception as exc:
        logger.warning("Could not persist QuickBooks credentials: %s", exc)


_qb_creds = _load_qb_credentials()
QB_CLIENT_ID = os.getenv("QB_CLIENT_ID", "") or _qb_creds.get("client_id", "")
QB_CLIENT_SECRET = os.getenv("QB_CLIENT_SECRET", "") or _qb_creds.get("client_secret", "")
QB_ACCESS_TOKEN = os.getenv("QB_ACCESS_TOKEN", "") or _qb_creds.get("access_token", "")
QB_REFRESH_TOKEN = os.getenv("QB_REFRESH_TOKEN", "") or _qb_creds.get("refresh_token", "")
QB_REALM_ID = os.getenv("QB_REALM_ID", "") or _qb_creds.get("realm_id", "")
QB_ENV = os.getenv("QB_ENV", "sandbox").lower()
QB_API = "https://quickbooks.api.intuit.com" if QB_ENV == "production" else "https://sandbox.quickbooks.api.intuit.com"
QB_REDIRECT_URI = os.getenv("QB_REDIRECT_URI", "http://localhost:8000/api/quickbooks/callback")
QB_AUTH_STATE: str = ""
PDF_PRICE_USD = float(os.getenv("PDF_PRICE_USD", "55.00"))
PLAN_PRICES = {"basic": 45.00, "gold": 65.00, "premium": 85.00}
PLAN_REPORTS = {"basic": 1, "gold": 2, "premium": 3}

GLOBALVIN_API_KEY = os.getenv("GLOBALVIN_API_KEY", "")
GLOBALVIN_BASE_URL = os.getenv("GLOBALVIN_BASE_URL", "https://globalvin.co/backend")
GLOBALVIN_ENABLED = bool(GLOBALVIN_API_KEY)

PDF_OWNER_PASSWORD = os.getenv("PDF_OWNER_PASSWORD") or secrets.token_hex(16)
# PDF permission bits (bit set = permitted): 0x4 print, 0x200 print-high-quality.
# Copy/extract text (0x10, 0x80), modify (0x8), fill/annotate (0x40, 0x20), assemble (0x100) are all denied.
PDF_ALLOW_ONLY_PRINT = 0x4 | 0x200


def validate_vin(vin: str) -> str:
    vin = vin.strip().upper()
    if len(vin) != 17:
        raise HTTPException(status_code=400, detail="VIN must be exactly 17 characters.")
    if re.search(r"[IOQ]", vin):
        raise HTTPException(status_code=400, detail="VIN cannot contain the letters I, O, or Q.")
    if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
        raise HTTPException(status_code=400, detail="VIN contains invalid characters.")
    if not check_vin_checksum(vin):
        raise HTTPException(status_code=400, detail="VIN failed the check digit (checksum) validation.")
    return vin


VIN_TRANSLITERATION = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def check_vin_checksum(vin: str) -> bool:
    if len(vin) != 17:
        return False
    total = 0
    for i, char in enumerate(vin):
        value = VIN_TRANSLITERATION.get(char)
        if value is None:
            return False
        total += value * VIN_WEIGHTS[i]
    check_char = "X" if total % 11 == 10 else str(total % 11)
    return check_char == vin[8]


class VinReport(BaseModel):
    vin: str
    vehicle: dict[str, Any] | None = None
    recalls: list[dict[str, Any]] = []
    complaints: list[dict[str, Any]] = []
    tsbs: list[dict[str, Any]] = []
    investigations: list[dict[str, Any]] = []
    safety: list[dict[str, Any]] = []
    fuel: dict[str, Any] | None = None
    vinaudit: dict[str, Any] | None = None  # GlobalVIN/Carfax NMVTIS data
    nmvtis_cost_usd: float = 0.0  # Cost of NMVTIS data query ($3 for Carfax)
    statuses: dict[str, str] = {}


async def fetch_vpic(vin: str) -> dict[str, Any] | None:
    cache_key = f"VPIC:{vin}"
    cached = LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(VPIC_URL.format(vin=vin))
        resp.raise_for_status()
        data = resp.json()
    results = data.get("Results") or []
    for r in results:
        if r.get("ErrorCode") not in (None, "", "0"):
            return None
    if not results:
        return None
    vehicle = results[0]
    if not vehicle.get("Make"):
        return None
    LOOKUP_CACHE.set(cache_key, vehicle)
    return vehicle


async def fetch_nhtsa_by_vehicle(endpoint: str, make: str, model: str, year: str) -> list[dict[str, Any]]:
    cache_key = f"{endpoint}:{make}|{model}|{year}"
    cached = LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached
    params = {"make": make, "model": model, "modelYear": year}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
    results = data.get("results") or data.get("Results") or []
    LOOKUP_CACHE.set(cache_key, results)
    return results


async def cache_photo(url: str) -> str:
    if not url:
        return ""
    name = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24] + ".jpg"
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    path = PHOTO_DIR / name
    if not path.exists():
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
                resp = await client.get(url)
                resp.raise_for_status()
            path.write_bytes(resp.content)
        except Exception as exc:
            logger.warning("Crash photo download failed (%s): %s", url, exc)
            return ""
    return path.as_uri()


def query_safety_db(make: str, model: str, year: str) -> list[dict[str, Any]]:
    with Session(engine) as session:
        rows = session.exec(
            select(SafetyRating)
            .where(func.upper(SafetyRating.make) == make.upper())
            .where(func.upper(SafetyRating.model) == model.upper())
            .where(SafetyRating.model_year == str(year))
            .limit(10)
        ).all()
    return [
        {
            "VehicleDescription": " ".join(
                x for x in [r.model_year, r.make, r.model, r.body_style or ""] if x
            ),
            "OverallFrontCrashRating": r.overall_frnt_stars,
            "OverallSideCrashRating": r.overall_side_stars,
            "SidePoleCrashRating": None,
            "RolloverRating": r.rollover_stars,
            "FrontCrashPicture": None,
            "SideCrashPicture": None,
            "SidePolePicture": None,
        }
        for r in rows
    ]


async def fetch_safety(make: str, model: str, year: str) -> list[dict[str, Any]]:
    cache_key = f"SAFETY:{make}|{model}|{year}"
    cached = LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached
    live_error: Exception | None = None
    ratings: list[dict[str, Any]] = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(
                SAFETY_BY_MODEL_URL.format(year=year, make=make, model=model),
            )
            resp.raise_for_status()
            matches = resp.json().get("Results") or []

            async def fetch_detail(match: dict[str, Any]) -> dict[str, Any] | None:
                vehicle_id = match.get("VehicleId")
                if not vehicle_id:
                    return None
                detail = await client.get(SAFETY_VEHICLE_URL.format(vehicle_id=vehicle_id))
                if detail.status_code != 200:
                    return None
                detail_results = detail.json().get("Results") or []
                return detail_results[0] if detail_results else None

            results = await asyncio.gather(*(fetch_detail(m) for m in matches))
        ratings = [r for r in results if r]
    except Exception as exc:
        live_error = exc
        logger.warning(
            "Safety ratings live lookup failed (%s %s %s): %s", make, model, year, exc
        )

    if not ratings:
        db_ratings = await asyncio.to_thread(query_safety_db, make, model, year)
        if db_ratings:
            ratings = db_ratings
        elif live_error is not None:
            raise live_error

    if ratings:
        cached_urls: dict[str, str] = {}
        for rating in ratings:
            for key in ("FrontCrashPicture", "SideCrashPicture", "SidePolePicture"):
                url = rating.get(key)
                if not url:
                    continue
                if url not in cached_urls:
                    cached_urls[url] = await cache_photo(url)
                rating[key] = cached_urls[url] or None

    LOOKUP_CACHE.set(cache_key, ratings)
    return ratings


def query_tsbs(make: str, model: str, year: str) -> list[dict[str, Any]]:
    model_norm = re.sub(r"\s+", "", model.upper())
    with Session(engine) as session:
        statement = (
            select(Tsb)
            .where(Tsb.make == make.upper())
            .where(Tsb.model_norm == model_norm)
            .where(
                or_(
                    Tsb.model_year == year,
                    Tsb.model_year == "",
                    Tsb.model_year == "9999",
                    Tsb.model_year.like(f"%{year}%"),
                )
            )
            .limit(50)
        )
        rows = session.exec(statement).all()
    return [
        {
            "doc_id": r.doc_id,
            "make": r.make,
            "model": r.model,
            "model_year": r.model_year,
            "summary": r.summary,
            "source_file": r.source_file,
        }
        for r in rows
    ]


def query_investigations(make: str, model: str, year: str) -> list[dict[str, Any]]:
    model_norm = re.sub(r"\s+", "", model.upper())
    with Session(engine) as session:
        statement = (
            select(Investigation)
            .where(Investigation.make == make.upper())
            .where(Investigation.model_norm == model_norm)
            .where(
                or_(
                    Investigation.year == year,
                    Investigation.year == "",
                    Investigation.year == "9999",
                    Investigation.year.like(f"%{year}%"),
                )
            )
            .limit(50)
        )
        rows = session.exec(statement).all()
    return [
        {
            "action_no": r.action_no,
            "make": r.make,
            "model": r.model,
            "year": r.year,
            "component": r.component,
            "mfr_name": r.mfr_name,
            "date_opened": r.date_opened,
            "date_closed": r.date_closed,
            "campno": r.campno,
            "subject": r.subject,
            "summary": r.summary,
        }
        for r in rows
    ]


async def fetch_fuel(make: str, model: str, year: str) -> dict[str, Any] | None:
    cache_key = f"FUEL:{make}|{model}|{year}"
    cached = LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached
    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
        options = await client.get(
            EPA_OPTIONS_URL.format(year=year, make=make, model=model),
        )
        options.raise_for_status()
        root = ET.fromstring(options.text)
        items = root.findall("menuItem")
        if not items:
            return None
        vehicle_id = (items[0].findtext("value") or "").strip()
        if not vehicle_id:
            return None
        detail = await client.get(EPA_VEHICLE_URL.format(vehicle_id=vehicle_id))
        if detail.status_code != 200:
            return None
        detail_root = ET.fromstring(detail.text)
        keys = [
            "make", "model", "year", "VClass", "trany", "drive",
            "cylinders", "displ", "fuelType", "fuelType1",
            "city08", "highway08", "comb08", "co2", "feScore",
            "ghgScore", "range", "mpgData",
        ]
        result = {k: detail_root.findtext(k) for k in keys}
    LOOKUP_CACHE.set(cache_key, result)
    return result


async def fetch_globalvin(vin: str) -> dict[str, Any] | None:
    """Fetch NMVTIS vehicle history from GlobalVIN API (Carfax report).

    Returns parsed Carfax data with keys:
        vehicle, highlights, accidents, services, title_history,
        ownership, detailed_events, additional_checks, odometer,
        damage_location, raw_pdf
    """
    if not GLOBALVIN_ENABLED:
        return None
    cache_key = f"GLOBALVIN:{vin}"
    cached = LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached

    headers = {
        "X-API-Key": GLOBALVIN_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            # Carfax report ($3/report, cached free if already pulled)
            url = GLOBALVIN_CARFAX_URL.format(base=GLOBALVIN_BASE_URL, vin=vin)
            resp = await client.get(url, headers=headers)

            if resp.status_code == 402:
                logger.warning("GlobalVIN insufficient credits for %s", vin)
                return None

            resp.raise_for_status()
            data = resp.json()

            if not data.get("success"):
                logger.warning("GlobalVIN Carfax report failed for %s: %s", vin, data.get("message"))
                return None

            raw = data.get("data") or {}
            report_b64 = raw.get("report", "")

            if not report_b64:
                logger.warning("GlobalVIN returned empty report for %s", vin)
                return None

            # Decode base64 PDF
            import base64
            pdf_bytes = base64.b64decode(report_b64)

            # Parse the Carfax PDF into structured data
            from carfax_parser import parse_carfax_pdf
            parsed = parse_carfax_pdf(pdf_bytes)

            # Store raw PDF bytes for direct Carfax download option
            parsed["raw_pdf"] = pdf_bytes
            parsed["report_id"] = raw.get("shortReportId", "")
            parsed["report_url"] = raw.get("reportUrl", "")

            LOOKUP_CACHE.set(cache_key, parsed)
            return parsed

    except Exception as exc:
        logger.warning("GlobalVIN lookup failed for %s: %s", vin, exc)
        return None


@app.get("/health")
@limiter.limit("60/minute")
async def health(request: Request) -> dict[str, str]:
    return {"status": "ok"}


def normalize_complaints(complaints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for c in complaints:
        components = c.get("components")
        if isinstance(components, list):
            component = ", ".join(str(x) for x in components)
        else:
            component = str(components) if components else ""
        normalized.append(
            {
                "ODTI": c.get("odiNumber"),
                "Component": component,
                "DateComplaintFiled": c.get("dateComplaintFiled"),
                "Summary": c.get("summary"),
                "dateOfIncident": c.get("dateOfIncident"),
                "crash": c.get("crash"),
                "fire": c.get("fire"),
                "numberOfDeaths": c.get("numberOfDeaths"),
                "numberOfInjuries": c.get("numberOfInjuries"),
                "manufacturer": c.get("manufacturer"),
                "products": c.get("products"),
            }
        )
    return normalized


async def build_report(vin: str) -> VinReport:
    vin = validate_vin(vin)
    cache_key = f"REPORT:{vin}"
    cached = REPORT_CACHE.get(cache_key)
    if cached is not None:
        return cached

    report = VinReport(vin=vin)

    try:
        vehicle = await fetch_vpic(vin)
    except Exception as exc:
        logger.warning("vPIC lookup failed for %s: %s", vin, exc)
        raise HTTPException(status_code=502, detail="Vehicle decode service unavailable.")
    if vehicle is None:
        raise HTTPException(status_code=404, detail="No vehicle found for this VIN.")
    report.vehicle = vehicle

    make = vehicle.get("Make") or ""
    model = vehicle.get("Model") or ""
    year = vehicle.get("ModelYear") or ""

    if make and model and year:
        statuses: dict[str, str] = {}

        async def run(label: str, coro) -> Any:
            try:
                result = await coro
            except Exception as exc:
                logger.warning("%s lookup failed: %s", label, exc)
                statuses[label] = "unavailable"
                return None
            statuses[label] = "ok"
            return result

        recalls, complaints, tsbs, investigations, safety, fuel, globalvin = await asyncio.gather(
            run("Recalls", fetch_nhtsa_by_vehicle(RECALLS_URL, make, model, year)),
            run("Complaints", fetch_nhtsa_by_vehicle(COMPLAINTS_URL, make, model, year)),
            run("TSB DB", asyncio.to_thread(query_tsbs, make, model, year)),
            run("Investigations DB", asyncio.to_thread(query_investigations, make, model, year)),
            run("Safety ratings", fetch_safety(make, model, year)),
            run("Fuel economy", fetch_fuel(make, model, year)),
            run("GlobalVIN", fetch_globalvin(vin)),
        )
        report.recalls = recalls or []
        report.complaints = normalize_complaints(complaints or [])
        report.tsbs = tsbs or []
        report.investigations = investigations or []
        report.safety = safety or []
        report.fuel = fuel
        report.vinaudit = globalvin
        report.nmvtis_cost_usd = 3.00 if globalvin else 0.0
        report.statuses = statuses

    REPORT_CACHE.set(cache_key, report)
    return report


@app.get("/api/vin/{vin}", response_model=VinReport)
@limiter.limit("30/minute")
async def get_vin_report(request: Request, vin: str) -> VinReport:
    return await build_report(vin)


@app.get("/api/vin/{vin}/decode")
@limiter.limit("30/minute")
async def decode_vin(request: Request, vin: str) -> dict[str, Any]:
    clean = validate_vin(vin)
    vpic = await fetch_vpic(clean)
    if not vpic:
        raise HTTPException(status_code=404, detail="Vehicle not found for this VIN")
    return {
        "vin": clean,
        "vehicle": {
            "Make": vpic.get("Make", ""),
            "Model": vpic.get("Model", ""),
            "ModelYear": vpic.get("ModelYear", ""),
            "Trim": vpic.get("Trim", ""),
            "BodyClass": vpic.get("BodyClass", ""),
            "DisplacementL": vpic.get("DisplacementL", ""),
            "EngineCylinders": vpic.get("EngineCylinders", ""),
            "EngineHP": vpic.get("EngineHP", ""),
            "FuelTypePrimary": vpic.get("FuelTypePrimary", ""),
            "DriveType": vpic.get("DriveType", ""),
            "Doors": vpic.get("Doors", ""),
            "TransmissionStyle": vpic.get("TransmissionStyle", ""),
            "PlantCity": vpic.get("PlantCity", ""),
            "PlantState": vpic.get("PlantState", ""),
            "PlantCountry": vpic.get("PlantCountry", ""),
            "Series": vpic.get("Series", ""),
            "VehicleType": vpic.get("VehicleType", ""),
            "ManufacturerName": vpic.get("ManufacturerName", ""),
        },
    }


@app.get("/api/vin/{vin}/pdf")
@limiter.limit("10/minute")
async def get_vin_pdf(request: Request, vin: str) -> Response:
    raise HTTPException(
        status_code=402,
        detail=(
            "Payment required. POST /api/vin/{vin}/pdf/checkout to create a "
            "payment, then POST /api/vin/{vin}/pdf/capture to download."
        ),
    )


@app.get("/api/vin/{vin}/pdf/preview")
@limiter.limit("30/minute")
async def get_vin_pdf_preview(request: Request, vin: str) -> Response:
    vin = validate_vin(vin)
    pdf = await render_pdf(vin)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{vin}-preview.pdf"',
            "Cache-Control": "no-store",
        },
    )


@app.post("/api/vin/{vin}/generate-report")
@limiter.limit("20/minute")
async def generate_plan_report(
    request: Request, vin: str, plan: str = Query("gold")
) -> Response:
    clean = validate_vin(vin)
    plan = plan.lower()
    if plan not in ("basic", "gold", "premium"):
        raise HTTPException(status_code=400, detail="Invalid plan. Must be basic, gold, or premium.")
    try:
        pdf = await render_pdf(clean, plan_id=plan)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to generate report: {e}")
    report_no = make_report_number(clean)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="CIP-{clean}-{plan}.pdf"',
            "X-Report-Number": report_no,
            "X-Plan": plan,
            "Cache-Control": "no-store",
        },
    )


# ---------------------------------------------------------------------------
# Paid PDF download (QuickBooks Payments)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Transform real API data into report template structures
# ---------------------------------------------------------------------------

def _build_real_highlights(report_data: dict[str, Any]) -> dict[str, Any]:
    """Derive summary highlight tiles from real NHTSA + parsed Carfax data."""
    complaints = report_data.get("complaints") or []
    recalls = report_data.get("recalls") or []
    vehicle = report_data.get("vehicle") or {}
    vn = report_data.get("vinaudit") or {}

    # Parsed Carfax data
    carfax = vn.get("parsed_carfax") or vn
    carfax_highlights = carfax.get("highlights") or {}

    # Accident detection: NHTSA complaints + Carfax accidents
    crash_complaints = [c for c in complaints if c.get("crash")]
    carfax_accidents = carfax.get("accidents") or []
    has_accident = bool(crash_complaints or carfax_accidents)

    severity = "minor damage"
    if crash_complaints:
        deaths = sum(int(c.get("numberOfDeaths") or 0) for c in crash_complaints)
        injuries = sum(int(c.get("numberOfInjuries") or 0) for c in crash_complaints)
        if deaths > 0 or injuries > 3:
            severity = "severe damage"
        elif injuries > 0:
            severity = "moderate damage"
    elif carfax_accidents:
        # Use Carfax severity
        sev = carfax_accidents[0].get("severity", "")
        severity = f"{sev} damage" if sev else "accident reported"

    # Odometer: from Carfax parsed data
    odometer = None
    carfax_odometer = carfax.get("odometer") or {}
    if carfax_odometer.get("current"):
        try:
            odometer = int(str(carfax_odometer["current"]).replace(",", ""))
        except (ValueError, TypeError):
            pass
    if not odometer:
        odo_raw = vehicle.get("Odometer")
        if odo_raw:
            try:
                odometer = int(str(odo_raw).replace(",", ""))
            except (ValueError, TypeError):
                pass

    # Owner count: from Carfax parsed data
    owners = carfax_highlights.get("owners") or 1
    if isinstance(owners, str):
        try:
            owners = int(owners)
        except ValueError:
            owners = 1

    highlights: dict[str, Any] = {}
    if has_accident:
        highlights["accident"] = True
        highlights["accident_severity"] = severity
    if odometer:
        highlights["odometer"] = odometer
    if owners:
        highlights["owners"] = owners
    if recalls:
        highlights["recalls"] = len(recalls)
    if complaints:
        highlights["complaints"] = len(complaints)

    return highlights


def _build_real_accidents(report_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Map NHTSA complaints + parsed Carfax accident records to accident/damage events."""
    complaints = report_data.get("complaints") or []
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn
    accidents: list[dict[str, Any]] = []

    # NHTSA crash complaints
    for c in complaints:
        if not c.get("crash"):
            continue
        deaths = int(c.get("numberOfDeaths") or 0)
        injuries = int(c.get("numberOfInjuries") or 0)
        if deaths > 0 or injuries > 2:
            sev = "severe"
        elif injuries > 0:
            sev = "moderate"
        else:
            sev = "minor"
        desc_parts = ["Involving a crash incident"]
        component = c.get("Component") or ""
        if component:
            desc_parts.append(f"Component: {component}")
        if deaths:
            desc_parts.append(f"{deaths} death(s) reported")
        if injuries:
            desc_parts.append(f"{injuries} injury(ies) reported")
        accidents.append({
            "type": f"{sev} damage" if sev != "minor" else "damage reported",
            "description": "; ".join(desc_parts),
            "severity": sev,
            "date": c.get("DateComplaintFiled") or c.get("dateOfIncident") or "",
            "airbags": "",
            "location": "",
        })

    # Parsed Carfax accident records
    for a in (carfax.get("accidents") or []):
        severity = a.get("severity", "minor")
        accidents.append({
            "type": f"{severity} damage",
            "description": a.get("description", "Accident reported"),
            "severity": severity,
            "date": a.get("date") or "",
            "airbags": "deployed" if "deployed" in (a.get("description") or "").lower() else "did not deploy",
            "location": carfax.get("damage_location", ""),
        })

    return accidents[:10]


def _build_real_services(report_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Build service section from parsed Carfax service records + recall remedies."""
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn
    recalls = report_data.get("recalls") or []
    services: list[dict[str, Any]] = []

    # Carfax service records (parsed from PDF)
    for s in (carfax.get("services") or [])[:20]:
        services.append({
            "type": "service",
            "service": s.get("service") or "Vehicle Service",
            "notes": s.get("notes") or "",
            "date": s.get("date") or "",
            "mileage": s.get("mileage") or "",
        })

    # Add recall remedies if not too many services already
    if len(services) < 20:
        for r in recalls[:6]:
            remedy = r.get("Remedy") or "Recall remedy available"
            date = r.get("ReportReceivedDate") or ""
            campaign = r.get("NHTSACampaignNumber") or ""
            services.append({
                "type": "recall",
                "service": f"Recall {campaign}" if campaign else "Manufacturer Recall",
                "notes": remedy[:120],
                "date": date,
                "mileage": "",
            })

    return services


def _build_real_additional_history(report_data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Build per-owner checks from parsed Carfax data + NHTSA data."""
    recalls = report_data.get("recalls") or []
    complaints = report_data.get("complaints") or []
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn

    # Parsed Carfax additional checks
    carfax_checks = carfax.get("additional_checks") or {}
    carfax_title = carfax.get("title_history") or {}

    crash_count = sum(1 for c in complaints if c.get("crash"))
    fire_count = sum(1 for c in complaints if c.get("fire"))
    airbag_complaints = [c for c in complaints if "airbag" in (c.get("Component") or "").lower()]
    odometer_complaints = [c for c in complaints if "odometer" in (c.get("Component") or "").lower() or "speedometer" in (c.get("Component") or "").lower()]

    checks: dict[str, str] = {}

    # Use Carfax parsed checks as primary source
    checks["total_loss"] = carfax_checks.get("total_loss", "No Issues Reported")
    checks["structural_damage"] = carfax_checks.get("structural_damage", "No Issues Reported")
    checks["airbag_deployment"] = carfax_checks.get("airbag_deployment", "No Issues Reported")
    checks["odometer_check"] = carfax_checks.get("odometer_check", "No Issues Indicated")
    checks["accident_damage"] = carfax_checks.get("accident_damage", "No Issues Reported")
    checks["manufacturer_recall"] = carfax_checks.get("manufacturer_recall", "No Recalls Reported")
    checks["basic_warranty"] = carfax_checks.get("basic_warranty", "Not Reported")

    # Title brands from parsed Carfax
    damage_clean = carfax_title.get("damage_brands_clean", True)
    odometer_clean = carfax_title.get("odometer_brands_clean", True)
    if damage_clean and odometer_clean:
        checks["title_brands"] = "Clean title"
    elif not damage_clean:
        brands = carfax_title.get("damage_brands") or []
        checks["title_brands"] = f"Brands: {', '.join(brands)}" if brands else "Title issues reported"
    else:
        checks["title_brands"] = "Odometer brand noted"

    # Theft: from parsed Carfax data
    checks["theft"] = carfax_checks.get("theft", "No Issues Reported")

    # Salvage/junk: from Carfax damage brands
    if not damage_clean:
        checks["salvage_junk"] = "Title brands present"
    else:
        checks["salvage_junk"] = "No Issues Reported"

    return {"owner_1": checks}


def _build_real_theft_records(report_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Build theft records from parsed Carfax data."""
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn

    # Parsed Carfax theft records
    carfax_theft = carfax.get("theft_records") or []
    if carfax_theft:
        return carfax_theft

    return []


def _build_real_title_history(report_data: dict[str, Any]) -> dict[str, Any]:
    """Build title history from parsed Carfax data."""
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn
    return carfax.get("title_history") or {}


def _build_real_ownership(report_data: dict[str, Any]) -> list[dict[str, str]]:
    """Build ownership summary from parsed Carfax ownership data."""
    vehicle = report_data.get("vehicle") or {}
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn
    year = vehicle.get("ModelYear") or ""

    # Parsed Carfax ownership
    carfax_ownership = carfax.get("ownership") or []

    if carfax_ownership:
        return carfax_ownership[:10]

    # Fallback: use Carfax highlights
    carfax_highlights = carfax.get("highlights") or {}
    owner_count = carfax_highlights.get("owners") or 1
    mileage = carfax_highlights.get("mileage") or ""

    return [{
        "number": "1",
        "year_purchased": str(year) if year else "—",
        "type": "Owner",
        "length_of_ownership": "—",
        "state": "—",
        "miles_per_year": "—",
        "odometer": str(mileage) if mileage else "—",
    }]


def _build_real_detailed_history(report_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Build chronological event history from NHTSA + parsed Carfax data."""
    vehicle = report_data.get("vehicle") or {}
    make = vehicle.get("Make") or ""
    model = vehicle.get("Model") or ""
    year = vehicle.get("ModelYear") or ""
    vin = report_data.get("vin") or ""
    model_label = f"{year} {make} {model}".strip()
    vn = report_data.get("vinaudit") or {}
    carfax = vn.get("parsed_carfax") or vn

    events: list[dict[str, Any]] = []

    # --- NHTSA complaints → damage/incident events ---
    for c in (report_data.get("complaints") or [])[:20]:
        crash = c.get("crash")
        fire = c.get("fire")
        deaths = int(c.get("numberOfDeaths") or 0)
        injuries = int(c.get("numberOfInjuries") or 0)
        component = c.get("Component") or "Unknown"
        summary_text = c.get("Summary") or ""
        date = c.get("DateComplaintFiled") or c.get("dateOfIncident") or ""
        comments = []
        if crash:
            comments.append("Crash incident reported")
        if fire:
            comments.append("Fire incident reported")
        if deaths:
            comments.append(f"{deaths} death(s) reported")
        if injuries:
            comments.append(f"{injuries} injury(ies) reported")
        comments.append(f"Component: {component}")
        if summary_text:
            comments.append(summary_text[:200])

        kind = "damage" if crash else ("fire" if fire else "complaint")
        events.append({
            "date": date,
            "mileage": "",
            "kind": kind,
            "source_name": "NHTSA Complaints",
            "source_loc": "U.S. DOT",
            "comments": comments,
            "severity": "severe" if deaths or injuries > 2 else ("moderate" if injuries else "minor"),
            "location": "",
        })

    # --- NHTSA recalls → recall events ---
    for r in (report_data.get("recalls") or [])[:10]:
        campaign = r.get("NHTSACampaignNumber") or ""
        component = r.get("Component") or ""
        summary_text = r.get("Summary") or ""
        consequence = r.get("Consequence") or ""
        remedy = r.get("Remedy") or ""
        date = r.get("ReportReceivedDate") or ""
        comments = []
        if component:
            comments.append(f"Component: {component}")
        if summary_text:
            comments.append(summary_text[:200])
        if consequence:
            comments.append(f"Consequence: {consequence[:150]}")
        if remedy:
            comments.append(f"Remedy: {remedy[:150]}")
        events.append({
            "date": date,
            "mileage": "",
            "kind": "recall",
            "source_name": f"NHTSA Recall {campaign}" if campaign else "NHTSA Recall",
            "source_loc": "U.S. DOT",
            "source_phone": "",
            "source_url": "nhtsa.gov/recalls",
            "comments": comments,
        })

    # --- TSBs → technical bulletin events ---
    for t in (report_data.get("tsbs") or [])[:10]:
        doc_id = t.get("doc_id") or ""
        summary_text = t.get("summary") or ""
        events.append({
            "date": "",
            "mileage": "",
            "kind": "tsb",
            "source_name": f"TSB {doc_id}" if doc_id else "Technical Service Bulletin",
            "source_loc": "Manufacturer",
            "comments": [summary_text[:300]] if summary_text else ["Technical Service Bulletin issued"],
        })

    # --- Investigations → investigation events ---
    for inv in (report_data.get("investigations") or [])[:10]:
        action = inv.get("action_no") or ""
        subject = inv.get("subject") or ""
        comp = inv.get("component") or ""
        opened = str(inv.get("date_opened") or "")
        closed = str(inv.get("date_closed") or "")
        comments = []
        if comp:
            comments.append(f"Component: {comp}")
        if subject:
            comments.append(subject[:200])
        if opened:
            comments.append(f"Opened: {opened}")
        if closed:
            comments.append(f"Closed: {closed}")
        events.append({
            "date": opened,
            "mileage": "",
            "kind": "investigation",
            "source_name": f"NHTSA Investigation {action}" if action else "NHTSA Investigation",
            "source_loc": "U.S. DOT",
            "comments": comments or ["Investigation recorded"],
        })

    # --- Parsed Carfax detailed events ---
    for ev in (carfax.get("detailed_events") or [])[:40]:
        kind = ev.get("kind", "service")
        # Map Carfax kinds to our kinds
        kind_map = {
            "service": "service",
            "damage": "damage",
            "title": "title",
            "ownership": "ownership",
            "sale": "sale",
            "certified": "sale",
        }
        mapped_kind = kind_map.get(kind, "service")

        source_name = ev.get("source_name", "")
        comments = ev.get("comments", [])

        events.append({
            "date": ev.get("date") or "",
            "mileage": ev.get("mileage") or "",
            "kind": mapped_kind,
            "source_name": f"Carfax — {source_name}" if source_name else "Carfax Record",
            "source_loc": "",
            "comments": comments if isinstance(comments, list) else [str(comments)],
        })

    # Sort all events by date (most recent first, blanks last)
    def _sort_key(ev: dict[str, Any]) -> str:
        d = ev.get("date") or "0000-00-00"
        return d
    events.sort(key=_sort_key, reverse=True)

    if not events:
        return []

    source_label = "NHTSA + Carfax records" if carfax else "NHTSA records"

    return [{
        "owner": 1,
        "purchased": str(year) if year else "",
        "note": f"Event history for {model_label} based on {source_label}.",
        "type": "NHTSA + Carfax" if carfax else "NHTSA Records",
        "miles_per_year": "—",
        "events": events,
    }]


async def render_pdf(vin: str, plan_id: str = "gold") -> bytes:
    cache_key = f"{vin}:{plan_id}"
    cached = PDF_CACHE.get(cache_key)
    if cached is not None:
        return cached
    report = await build_report(vin)
    report_data = report.model_dump()
    report_no = make_report_number(vin)
    issued_on = datetime.now().strftime("%B %d, %Y")

    real_highlights = _build_real_highlights(report_data)
    real_accidents = _build_real_accidents(report_data)
    real_services = _build_real_services(report_data)
    real_checks = _build_real_additional_history(report_data)
    real_ownership = _build_real_ownership(report_data)
    real_detailed = _build_real_detailed_history(report_data)
    real_theft = _build_real_theft_records(report_data)
    real_title = _build_real_title_history(report_data)

    nmvtis_available = report_data.get("vinaudit") is not None

    html_doc = build_report_html(
        report_data,
        report_no,
        issued_on,
        highlights=real_highlights or None,
        accidents=real_accidents or None,
        services=real_services or None,
        owners_history_checks=real_checks,
        owners_ownership=real_ownership,
        detailed_history=real_detailed or None,
        theft_records=real_theft or None,
        title_history=real_title or None,
        nmvtis_available=nmvtis_available,
        plan_id=plan_id,
    )
    try:
        from weasyprint import HTML

        pdf = HTML(string=html_doc, base_url=str(Path(__file__).resolve().parent)).write_pdf()
    except Exception as exc:
        logger.exception("PDF generation failed")
        raise HTTPException(
            status_code=503,
            detail=(
                "PDF generation is unavailable on this system (WeasyPrint needs "
                "the GTK3 runtime on Windows). Install the GTK3 runtime and "
                "restart the server, or use the web report."
            ),
        )
    pdf = protect_pdf(pdf)
    PDF_CACHE.set(cache_key, pdf)
    return pdf


def protect_pdf(pdf: bytes) -> bytes:
    """Encrypt the PDF with an empty user password and owner password.

    Users can open/print without a password, but the viewer should deny text
    copying/extraction and modification. This is advisory DRM, not bulletproof.
    """
    if not PDF_PROTECTION_AVAILABLE:
        return pdf
    try:
        reader = PdfReader(BytesIO(pdf))
        writer = PdfWriter()
        writer.append(reader)
        writer.encrypt(
            user_password="",
            owner_password=PDF_OWNER_PASSWORD,
            permissions_flag=PDF_ALLOW_ONLY_PRINT,
        )
        out = BytesIO()
        writer.write(out)
        return out.getvalue()
    except Exception as exc:
        logger.warning("PDF protection failed, returning unprotected PDF: %s", exc)
        return pdf


def frontend_origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


def prune_pending_orders() -> None:
    now = time.time()
    stale = [k for k, o in PENDING_ORDERS.items() if now - o.get("created_at", 0) > 3600]
    for k in stale:
        PENDING_ORDERS.pop(k, None)


async def qb_refresh_access_token() -> dict[str, str]:
    """Refresh QuickBooks OAuth2 access token using refresh token."""
    global QB_ACCESS_TOKEN, QB_REFRESH_TOKEN
    if not QB_REFRESH_TOKEN:
        raise HTTPException(status_code=503, detail="QuickBooks OAuth not configured. Complete the OAuth flow first.")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
            data={
                "grant_type": "refresh_token",
                "refresh_token": QB_REFRESH_TOKEN,
            },
            headers={
                "Authorization": f"Basic {base64.b64encode(f'{QB_CLIENT_ID}:{QB_CLIENT_SECRET}'.encode()).decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        resp.raise_for_status()
        data = resp.json()
    QB_ACCESS_TOKEN = data["access_token"]
    if data.get("refresh_token"):
        QB_REFRESH_TOKEN = data["refresh_token"]
    _save_qb_credentials(access_token=QB_ACCESS_TOKEN, refresh_token=QB_REFRESH_TOKEN)
    return {"access_token": QB_ACCESS_TOKEN, "refresh_token": QB_REFRESH_TOKEN}


async def qb_get_access_token() -> str:
    """Return a valid QuickBooks access token, refreshing if needed."""
    if not QB_ACCESS_TOKEN:
        result = await qb_refresh_access_token()
        return result["access_token"]
    return QB_ACCESS_TOKEN


async def qb_create_charge(vin: str, card_token: str, amount_usd: float) -> dict[str, Any]:
    """Create a payment charge via QuickBooks Payments API."""
    token = await qb_get_access_token()
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            f"{QB_API}/v3/company/{QB_REALM_ID}/payments/charge",
            json={
                "amount": f"{amount_usd:.2f}",
                "capture": True,
                "card": {
                    "token": card_token,
                },
                "description": f"Car Inspection Pro VIN Report PDF — {vin}",
                "custom_id": vin,
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        if resp.status_code == 401:
            await qb_refresh_access_token()
            token = await qb_get_access_token()
            resp = await client.post(
                f"{QB_API}/v3/company/{QB_REALM_ID}/payments/charge",
                json={
                    "amount": f"{amount_usd:.2f}",
                    "capture": True,
                    "card": {"token": card_token},
                    "description": f"Car Inspection Pro VIN Report PDF — {vin}",
                    "custom_id": vin,
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
        resp.raise_for_status()
        return resp.json()


@app.post("/api/vin/{vin}/pdf/checkout")
@limiter.limit("10/minute")
async def pdf_checkout(request: Request, vin: str) -> dict[str, Any]:
    """Checkout endpoint — frontend sends card token from Intuit.js SDK."""
    vin = validate_vin(vin)
    body = await request.json()
    card_token = body.get("card_token")
    if not card_token:
        raise HTTPException(status_code=400, detail="card_token is required.")
    plan = str(body.get("plan") or "").lower()
    if plan and plan not in PLAN_PRICES:
        raise HTTPException(
            status_code=400, detail="Invalid plan. Must be basic, gold, or premium."
        )
    price_usd = PLAN_PRICES.get(plan, PDF_PRICE_USD)
    reports = PLAN_REPORTS.get(plan, 1)

    await render_pdf(vin)
    prune_pending_orders()

    try:
        result = await qb_create_charge(vin, card_token, price_usd)
    except httpx.HTTPStatusError as exc:
        logger.warning("QuickBooks charge failed for %s: %s", vin, exc.response.text)
        raise HTTPException(status_code=402, detail="Payment was declined.")
    except Exception as exc:
        logger.warning("QuickBooks charge error for %s: %s", vin, exc)
        raise HTTPException(status_code=502, detail="Payment service unavailable.")

    payment_id = result.get("payments", [{}])[0].get("id") if isinstance(result.get("payments"), list) else result.get("id")
    PENDING_ORDERS[str(payment_id)] = {
        "vin": vin,
        "provider": "quickbooks",
        "payment_id": payment_id,
        "plan": plan,
        "created_at": time.time(),
    }
    return {
        "order_id": str(payment_id),
        "provider": "quickbooks",
        "price_usd": price_usd,
        "plan": plan,
        "reports": reports,
    }


@app.post("/api/vin/{vin}/pdf/capture")
@limiter.limit("10/minute")
async def pdf_capture(request: Request, vin: str, order_id: str) -> Response:
    vin = validate_vin(vin)
    order = PENDING_ORDERS.get(order_id)
    if not order or order.get("vin") != vin:
        raise HTTPException(status_code=403, detail="Unknown or mismatched payment order.")
    if order["provider"] != "quickbooks":
        raise HTTPException(status_code=403, detail="Unknown payment provider.")
    payment_id = order.get("payment_id")
    if payment_id:
        token = await qb_get_access_token()
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(
                f"{QB_API}/v3/company/{QB_REALM_ID}/payments/charge/{payment_id}",
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            )
            if resp.ok:
                data = resp.json()
                status = data.get("payments", [{}])[0].get("status") if isinstance(data.get("payments"), list) else data.get("status")
                if status not in ("captured", "settled", "ChargeSuccessful", "ChargeCaptured", "SettledSuccessfully"):
                    raise HTTPException(status_code=402, detail=f"Payment not yet completed (status: {status}).")

    pdf = await render_pdf(vin)
    prune_pending_orders()
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{vin}.pdf"',
            "Cache-Control": "no-store",
        },
    )


@app.get("/api/quickbooks/auth")
@limiter.limit("5/minute")
async def qb_auth(request: Request) -> dict[str, str]:
    """Return QuickBooks OAuth authorization URL for one-time setup."""
    if not QB_CLIENT_ID:
        raise HTTPException(status_code=503, detail="QuickBooks Client ID not configured.")
    global QB_AUTH_STATE
    QB_AUTH_STATE = secrets.token_urlsafe(32)
    auth_url = (
        f"https://appcenter.intuit.com/app/connect/oauth2"
        f"?client_id={QB_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=com.intuit.quickbooks.payment"
        f"&redirect_uri={QB_REDIRECT_URI}"
        f"&state={QB_AUTH_STATE}"
    )
    return {"authorization_url": auth_url, "state": QB_AUTH_STATE}


@app.get("/api/quickbooks/status")
@limiter.limit("60/minute")
async def qb_status(request: Request) -> dict[str, Any]:
    """Expose QuickBooks connectivity state for the frontend checkout."""
    return {
        "configured": bool(
            QB_CLIENT_ID and QB_CLIENT_SECRET and QB_ACCESS_TOKEN and QB_REFRESH_TOKEN and QB_REALM_ID
        ),
        "client_id": QB_CLIENT_ID or None,
        "env": QB_ENV,
        "realm_id": QB_REALM_ID or None,
    }


@app.get("/api/quickbooks/callback")
async def qb_callback(code: str = "", state: str = "", error: str = "") -> HTMLResponse:
    """OAuth callback — exchanges code for access + refresh tokens and persists them."""
    if error:
        return HTMLResponse(f"<h1>Authorization failed</h1><p>{error}</p>", status_code=400)
    if not code:
        return HTMLResponse("<h1>Authorization failed</h1><p>No authorization code received.</p>", status_code=400)
    if not state or not QB_AUTH_STATE or not secrets.compare_digest(state, QB_AUTH_STATE):
        return HTMLResponse("<h1>Authorization failed</h1><p>Invalid OAuth state.</p>", status_code=403)
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": QB_REDIRECT_URI,
            },
            headers={
                "Authorization": f"Basic {base64.b64encode(f'{QB_CLIENT_ID}:{QB_CLIENT_SECRET}'.encode()).decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        if not resp.ok:
            return HTMLResponse(f"<h1>Token exchange failed</h1><p>{resp.text}</p>", status_code=500)
        data = resp.json()
    global QB_ACCESS_TOKEN, QB_REFRESH_TOKEN, QB_REALM_ID
    QB_ACCESS_TOKEN = data.get("access_token", "")
    QB_REFRESH_TOKEN = data.get("refresh_token", "")
    QB_REALM_ID = str(data.get("realmId") or QB_REALM_ID)
    _save_qb_credentials(
        client_id=QB_CLIENT_ID,
        client_secret=QB_CLIENT_SECRET,
        access_token=QB_ACCESS_TOKEN,
        refresh_token=QB_REFRESH_TOKEN,
        realm_id=QB_REALM_ID,
    )
    return HTMLResponse(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>QuickBooks Connected</title>
<style>body {{ font-family: system-ui; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; background:#f1f5f9; }}
.box {{ background:#fff; padding:40px; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,.08); text-align:center; max-width:520px; }}
h1 {{ color:#0f172a; margin:0 0 12px; }} p {{ color:#64748b; line-height:1.5; }} .ok {{ color:#16a34a; font-weight:700; }}
code {{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:2px 6px; }}</style></head>
<body><div class="box"><h1>QuickBooks Connected</h1>
<p class="ok">Authorization successful — tokens saved to the server.</p>
<p>Realm / company ID: <code>{QB_REALM_ID}</code><br>Environment: <code>{QB_ENV}</code></p>
<p>You can close this window. On-site card checkout is now enabled.</p>
</div></body></html>""")
