"""Parse Carfax PDF text into structured data for Car Inspection Pro template.

Carfax reports have a very consistent format:
  Page 1: Summary (vehicle, accident, service, owners, mileage)
  Page 2: Additional History (total loss, structural, airbag, odometer, title brands)
  Page 3-8: Detailed History (chronological events per owner)
  Page 9-10: Glossary

This parser extracts structured JSON from the PDF text.
"""

import re
from typing import Any


def parse_carfax_pdf(pdf_bytes: bytes) -> dict[str, Any]:
    """Parse a Carfax PDF into structured data for the Car Inspection Pro template.

    Returns a dict with keys matching what render_pdf() expects:
      vehicle, highlights, accidents, services, title_history,
      ownership, detailed_events, additional_checks
    """
    from pypdf import PdfReader
    from io import BytesIO

    reader = PdfReader(BytesIO(pdf_bytes))
    pages = [p.extract_text() or "" for p in reader.pages]
    full_text = "\n".join(pages)

    result: dict[str, Any] = {}

    result["vehicle"] = _parse_vehicle_summary(full_text, pages[0])
    result["highlights"] = _parse_highlights(full_text, pages[0])
    result["accidents"] = _parse_accidents(full_text)
    result["services"] = _parse_services(full_text)
    result["title_history"] = _parse_title_brands(full_text, pages[1] if len(pages) > 1 else "")
    result["ownership"] = _parse_ownership(full_text)
    result["detailed_events"] = _parse_detailed_history(full_text)
    result["additional_checks"] = _parse_additional_checks(pages[1] if len(pages) > 1 else full_text)
    result["odometer"] = _parse_odometer(full_text, pages[0])
    result["damage_location"] = _parse_damage_location(full_text)
    result["theft_records"] = _parse_theft_records(full_text)

    return result


# ---------------------------------------------------------------------------
# Vehicle summary (page 1)
# ---------------------------------------------------------------------------

def _parse_vehicle_summary(full_text: str, page1: str) -> dict[str, Any]:
    """Extract year, make, model, trim, mileage, VIN, body, engine, fuel, drive."""
    vehicle: dict[str, Any] = {}

    # Line like: "2015 Chevrolet Cruze 1LT Auto"
    m = re.search(r"(\d{4})\s+([\w\s]+?)\s+(\w+)\s+(\w+\s+\w+)", page1)
    if m:
        vehicle["year"] = m.group(1)
        vehicle["make"] = m.group(2).strip()
        vehicle["model"] = m.group(3).strip()
        vehicle["trim"] = m.group(4).strip()
    else:
        # Simpler pattern
        m2 = re.search(r"(\d{4})\s+([\w]+)\s+([\w]+)", page1)
        if m2:
            vehicle["year"] = m2.group(1)
            vehicle["make"] = m2.group(2)
            vehicle["model"] = m2.group(3)
            vehicle["trim"] = ""

    # Mileage: "138,813 mi"
    m = re.search(r"([\d,]+)\s*mi", page1)
    if m:
        vehicle["mileage"] = m.group(1).replace(",", "")

    # VIN
    m = re.search(r"VIN:(\w{17})", page1)
    if m:
        vehicle["vin"] = m.group(1)

    # Body: "Sedan 4 DR"
    m = re.search(r"(Sedan|SUV|Truck|Coupe|Hatchback|Wagon|Van|Cab)\s*\d*\s*(DR|door)?", page1, re.I)
    if m:
        vehicle["body"] = m.group(0).strip()

    # Engine: "1.4L I4 F DOHC 16V"
    m = re.search(r"(\d+\.\d+L\s+\w+[\w\s]*?(?:DOHC|SOHC|OHV|VVT)[\w\s]*?\d*V?)", page1)
    if m:
        vehicle["engine"] = m.group(1).strip()

    # Fuel
    m = re.search(r"(Gasoline|Diesel|Electric|Hybrid|Flex Fuel|E85)", page1, re.I)
    if m:
        vehicle["fuel"] = m.group(1)

    # Drive
    m = re.search(r"(Front wheel drive|Rear wheel drive|All wheel drive|4WD|AWD|FWD|RWD)", page1, re.I)
    if m:
        vehicle["drive"] = m.group(1)

    return vehicle


# ---------------------------------------------------------------------------
# Highlights / summary tiles
# ---------------------------------------------------------------------------

def _parse_highlights(full_text: str, page1: str) -> dict[str, Any]:
    """Extract accident count, owner count, service count, mileage."""
    highlights: dict[str, Any] = {}

    # Owners
    m = re.search(r"(\d+)\s+Previous\s+Owners?", page1, re.I)
    if m:
        highlights["owners"] = int(m.group(1))

    # Service records count
    m = re.search(r"(\d+)\s+Service\s+History\s+Records?", page1, re.I)
    if m:
        highlights["service_count"] = int(m.group(1))

    # Mileage
    m = re.search(r"([\d,]+)\s*mi", page1)
    if m:
        highlights["mileage"] = m.group(1).replace(",", "")

    # Accident count
    accidents = re.findall(r"Accident reported", full_text, re.I)
    highlights["accident_count"] = len(accidents) if accidents else 0

    # History-based value
    m = re.search(r"\$([\d,]+)\s*CARFAX\s*Retail\s*Value", page1)
    if m:
        highlights["retail_value"] = m.group(1).replace(",", "")

    return highlights


# ---------------------------------------------------------------------------
# Accident / damage records
# ---------------------------------------------------------------------------

def _parse_accidents(full_text: str) -> list[dict[str, Any]]:
    """Extract all accident/damage events."""
    accidents: list[dict[str, Any]] = []

    # Pattern: "MM/DD/YYYY Accident reported: minor damage"
    # followed by description lines
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{4})\s*Accident reported:\s*(minor damage|moderate damage|severe damage|damage reported)",
        re.I,
    )

    for m in pattern.finditer(full_text):
        date = m.group(1)
        severity_text = m.group(2).strip()

        # Get context after match (next 300 chars for description)
        start = m.end()
        context = full_text[start:start + 500]

        # Extract damage details
        description_parts = []
        if "front" in context.lower() or "side" in context.lower():
            impacts = re.findall(r"(front|side|rear)\s*(?:or\s*(front|side|rear))?\s*impact", context, re.I)
            if impacts:
                description_parts.append(f"Involving {'/'.join(impacts[0])} impact")

        if "another motor vehicle" in context.lower():
            description_parts.append("with another motor vehicle")

        if "airbag" in context.lower():
            if "did not deploy" in context.lower():
                description_parts.append("Airbags did not deploy")
            elif "deployed" in context.lower():
                description_parts.append("Airbags deployed")

        # Damage severity
        severity = "minor"
        if "moderate" in severity_text.lower():
            severity = "moderate"
        elif "severe" in severity_text.lower():
            severity = "severe"

        accidents.append({
            "date": date,
            "severity": severity,
            "severity_text": severity_text,
            "description": "; ".join(description_parts) if description_parts else "Accident reported",
        })

    return accidents


# ---------------------------------------------------------------------------
# Service records
# ---------------------------------------------------------------------------

def _parse_services(full_text: str) -> list[dict[str, Any]]:
    """Extract service records from detailed history."""
    services: list[dict[str, Any]] = []

    # Carfax services appear as:
    # "MM/DD/YYYY Mileage Dealer NameCity, StatePhone"
    # "Vehicle serviced"
    # "Service1Service2Service3"

    # Find all "Vehicle serviced" entries
    # Pattern: date + mileage + location + "Vehicle serviced" + service items
    blocks = re.split(r"(?=\d{2}/\d{2}/\d{4}\s+[\d,]+\s+)", full_text)

    for block in blocks:
        if "Vehicle serviced" not in block:
            continue

        # Extract date
        date_match = re.match(r"(\d{2}/\d{2}/\d{4})", block)
        if not date_match:
            continue
        date = date_match.group(1)

        # Extract mileage
        mile_match = re.search(r"\d{2}/\d{2}/\d{4}\s+([\d,]+)", block)
        mileage = mile_match.group(1) if mile_match else ""

        # Extract service comments (everything after "Vehicle serviced")
        serviced_idx = block.find("Vehicle serviced")
        if serviced_idx == -1:
            continue
        comments_raw = block[serviced_idx + len("Vehicle serviced"):]

        # Clean up aggressively - remove all non-service text
        # Stop at next date, phone number, URL, rating, or review count
        comments = re.split(
            r"(?:\d{2}/\d{2}/\d{4}|\d{3}-\d{3}-\d{4}|https?://|\d+\.\d+\s*/\s*5\.0|\d+\s+Verified|\d+\s+Customer|Ohio|Pennsylvania|Texas|California|New York)",
            comments_raw
        )[0]

        # Clean whitespace and join
        comments = re.sub(r"\s+", " ", comments).strip()

        # Remove trailing "Vehicle serviced" if duplicated
        comments = comments.replace("Vehicle serviced", "").strip()

        # Fix concatenated words: "completedOil" → "completed, Oil"
        comments = re.sub(r"([a-z])([A-Z])", r"\1, \2", comments)
        # Fix "changed 01" → "changed. 01" (date bleeding into text)
        comments = re.sub(r"changed (\d{2}/)", r"changed. \1", comments)

        if comments:
            services.append({
                "date": date,
                "mileage": mileage,
                "type": "service",
                "service": "Vehicle Service",
                "notes": comments[:200],
            })

    return services[:30]


# ---------------------------------------------------------------------------
# Title brands / history check
# ---------------------------------------------------------------------------

def _parse_title_brands(full_text: str, page2: str) -> dict[str, Any]:
    """Extract title brand information."""
    result: dict[str, Any] = {
        "damage_brands": [],
        "odometer_brands": [],
    }

    # Damage brands: "Salvage | Junk | Rebuilt | Fire | Flood | Hail | Lemon GuaranteedNo Problem"
    if "GuaranteedNo Problem" in page2 or "Guaranteed No Problem" in page2:
        result["damage_brands_clean"] = True
    elif any(brand in page2 for brand in ["Salvage", "Junk", "Rebuilt", "Fire", "Flood"]):
        result["damage_brands_clean"] = False
        for brand in ["Salvage", "Junk", "Rebuilt", "Fire", "Flood", "Hail", "Lemon"]:
            if brand in page2:
                result["damage_brands"].append(brand)
    else:
        result["damage_brands_clean"] = True

    # Odometer brands
    if "Not Actual Mileage" in page2 or "Exceeds Mechanical Limits" in page2:
        result["odometer_brands_clean"] = False
    else:
        result["odometer_brands_clean"] = True

    return result


# ---------------------------------------------------------------------------
# Ownership history
# ---------------------------------------------------------------------------

def _parse_ownership(full_text: str) -> list[dict[str, Any]]:
    """Extract ownership history from both the summary table and detailed sections."""
    owners: list[dict[str, Any]] = []

    # --- Method 1: Parse the ownership summary table on page 2 ---
    # Format: "Year purchased 2015 2021 2025"
    #          "Type of owner See Details Personal Personal"
    #          "Estimated length of ownership 6 yrs. 5 mo. 3 yrs. 10 mo. 11 months"
    #          "Owned in the following states/provinces Ohio, Ohio Ohio Ohio"
    #          "Last reported odometer reading 64,602 128,595 138,813"

    years_match = re.search(r"Year purchased\s+((?:\d{4}\s*)+)", full_text)
    types_match = re.search(r"Type of owner\s+(See Details\s+)?((?:Personal(?:\s+Lease)?|Fleet|Commercial)\s*(?:Personal(?:\s+Lease)?|Fleet|Commercial|\s+)*)", full_text)
    lengths_match = re.search(r"Estimated length of ownership\s+([\d]+\s*(?:yr|mo|month|year)[\w\s.,]+?)(?:\n|Owned)", full_text, re.I)
    states_match = re.search(r"Owned in the following states/provinces\s+([\w\s,]+?)(?:\n|Last)", full_text)
    odometers_match = re.search(r"Last reported odometer reading\s+([\d,]+(?:\s+[\d,]+)*)", full_text)

    if years_match:
        years = years_match.group(1).strip().split()
        types_raw = types_match.group(2).strip() if types_match else ""
        types = types_raw.split() if types_raw else ["Personal"] * len(years)
        # Pad types if shorter than years
        while len(types) < len(years):
            types.append("Personal")

        lengths_raw = lengths_match.group(1).strip() if lengths_match else ""
        # Split ownership lengths - they're separated by spaces but contain multi-word entries
        # e.g. "6 yrs. 5 mo. 3 yrs. 10 mo. 11 months"
        length_parts = re.findall(r"[\d]+\s*(?:yr|mo|month|year|yrs|months?)\.?", lengths_raw)

        states_raw = states_match.group(1).strip() if states_match else ""
        # States are space-separated but may have commas: "Ohio, Ohio Ohio Ohio"
        state_parts = re.sub(r",\s*", " ", states_raw).split()

        odometers_raw = odometers_match.group(1) if odometers_match else ""
        odo_parts = odometers_raw.split()

        for i, year in enumerate(years):
            owner_type = types[i] if i < len(types) else "Personal"
            # Combine "Personal" + "Lease" if needed
            if owner_type == "Lease" and i > 0 and types[i-1] == "Personal":
                owner_type = "Personal Lease"

            length = length_parts[i] if i < len(length_parts) else ""
            state = state_parts[i] if i < len(state_parts) else ""
            odo = odo_parts[i] if i < len(odo_parts) else ""

            owners.append({
                "number": str(i + 1),
                "year_purchased": year,
                "type": owner_type,
                "length_of_ownership": length,
                "state": state,
                "miles_per_year": "",
                "odometer": odo.replace(",", ""),
            })

    # --- Method 2: Parse detailed owner sections for accurate count ---
    # The summary table may group "Owners 1-2" as one column
    # So we also count from the detailed sections
    detailed_owners: list[dict[str, Any]] = []
    owner_blocks = re.split(r"(?=Owner\s+\d+Purchased:)", full_text)
    for block in owner_blocks:
        m = re.match(r"Owner\s+(\d+)Purchased:(\d{4})", block)
        if not m:
            continue
        owner_num = m.group(1)
        year = m.group(2)

        owner_type = "Personal"
        if "Personal Lease" in block[:500]:
            owner_type = "Personal Lease"

        length = ""
        m_len = re.search(r"(\d+\s*(?:yr|mo|month|year)[\w\s.]*)", block[:500])
        if m_len:
            length = m_len.group(1).strip()

        mpy = re.search(r"([\d,]+)/yr", block)
        miles_per_year = mpy.group(1) + "/yr" if mpy else ""

        odo = re.findall(r"([\d,]+)", block)
        last_odo = ""
        for o in reversed(odo):
            clean = o.replace(",", "")
            # Odometer should be 2-6 digits, not title numbers (10 digits) or VIN fragments
            if clean.isdigit() and 100 <= int(clean) <= 999999:
                last_odo = clean
                break

        detailed_owners.append({
            "number": owner_num,
            "year_purchased": year,
            "type": owner_type,
            "length_of_ownership": length,
            "state": "",
            "miles_per_year": miles_per_year,
            "odometer": last_odo,
        })

    # Use detailed owners if more than summary (summary groups 1-2)
    if len(detailed_owners) > len(owners):
        owners = detailed_owners
    elif not owners:
        owners = detailed_owners

    # Clear odometer from detailed sections (unreliable) - will be enriched from summary
    for owner in owners:
        owner["odometer"] = ""
        owner["miles_per_year"] = ""

    # --- Enrich with odometer from summary table ---
    # Summary table may have fewer columns than owners (e.g., "Owners 1-2" grouped)
    # When grouped, the first column covers multiple owners
    odometers_match = re.search(r"Last reported odometer reading\s+([\d,]+(?:\s+[\d,]+)*)", full_text)
    if odometers_match and owners:
        odo_parts = odometers_match.group(1).split()
        if len(odo_parts) >= len(owners):
            # One-to-one mapping
            for i, owner in enumerate(owners):
                owner["odometer"] = odo_parts[i].replace(",", "")
        elif len(odo_parts) > 0:
            # Fewer odometer values than owners (first column groups owners)
            # Map first value to owner 1, then skip to remaining
            owners[0]["odometer"] = odo_parts[0].replace(",", "")
            # Remaining owners get the remaining values
            for i in range(1, len(odo_parts)):
                owner_idx = len(owners) - len(odo_parts) + i
                if 0 <= owner_idx < len(owners):
                    owners[owner_idx]["odometer"] = odo_parts[i].replace(",", "")

    # --- Enrich with miles_per_year from summary table ---
    mpy_match = re.search(r"Estimated miles driven per year\s+(?:See Details\s+)?((?:[\d,]+/yr\s*)+)", full_text)
    if mpy_match and owners:
        mpy_parts = re.findall(r"([\d,]+/yr)", mpy_match.group(1))
        for i, owner in enumerate(owners):
            if i < len(mpy_parts):
                owner["miles_per_year"] = mpy_parts[i]

    return owners


# ---------------------------------------------------------------------------
# Detailed history (chronological events)
# ---------------------------------------------------------------------------

def _parse_detailed_history(full_text: str) -> list[dict[str, Any]]:
    """Extract chronological service + event records."""
    events: list[dict[str, Any]] = []

    # Find all dated entries in the detailed history section
    # Patterns:
    # "MM/DD/YYYY 里程 DealerLocationPhone"
    # "MM/DD/YYYY StateMotor Vehicle Dept.LocationTitle #XXXXX"

    # Split by date patterns
    lines = re.split(r"\n", full_text)

    current_date = ""
    current_mileage = ""
    current_source = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Date + mileage pattern: "08/06/2023 Damage Report..."
        date_mile = re.match(r"^(\d{2}/\d{2}/\d{4})\s+([\d,]+)?\s*(.*)", line)
        if date_mile:
            current_date = date_mile.group(1)
            current_mileage = date_mile.group(2) or ""
            rest = date_mile.group(3).strip()

            if "Vehicle serviced" in rest:
                # Service event
                services_text = rest.replace("Vehicle serviced", "").strip()
                services_text = re.sub(r"\d{3}-\d{3}-\d{4}.*", "", services_text).strip()
                services_text = re.sub(r"https?://\S+.*", "", services_text).strip()
                services_text = re.sub(r"\d+\.\d+\s*/\s*5\.0.*", "", services_text).strip()
                services_text = re.sub(r"\d+\s+Verified Reviews.*", "", services_text).strip()
                services_text = re.sub(r"\d+\s+Customer Favorites.*", "", services_text).strip()

                if services_text:
                    events.append({
                        "date": current_date,
                        "mileage": current_mileage,
                        "kind": "service",
                        "source_name": current_source or "Service Center",
                        "comments": [services_text[:300]],
                    })
            elif "Accident reported" in rest or "Damage Report" in rest:
                events.append({
                    "date": current_date,
                    "mileage": current_mileage,
                    "kind": "damage",
                    "source_name": "Accident Report",
                    "comments": [rest[:300]],
                })
            elif "Title issued" in rest or "Registration issued" in rest:
                events.append({
                    "date": current_date,
                    "mileage": current_mileage,
                    "kind": "title",
                    "source_name": "Motor Vehicle Dept.",
                    "comments": [rest[:200]],
                })
            elif "Vehicle purchase reported" in rest:
                events.append({
                    "date": current_date,
                    "mileage": current_mileage,
                    "kind": "ownership",
                    "source_name": "Motor Vehicle Dept.",
                    "comments": ["Vehicle purchase reported"],
                })
            elif "offered for sale" in rest.lower() or "Offered for sale" in rest:
                events.append({
                    "date": current_date,
                    "mileage": current_mileage,
                    "kind": "sale",
                    "source_name": "Dealer",
                    "comments": [rest[:200]],
                })
            elif "Certified Pre-Owned" in rest:
                events.append({
                    "date": current_date,
                    "mileage": current_mileage,
                    "kind": "certified",
                    "source_name": "Certified Pre-Owned",
                    "comments": [rest[:200]],
                })

        # Source line (dealer/service center)
        elif re.search(r"\d{3}-\d{3}-\d{4}", line):
            # This is a dealer/service line
            current_source = re.sub(r"\d{3}-\d{3}-\d{4}.*", "", line).strip()
            current_source = re.sub(r"https?://\S+.*", "", current_source).strip()
            current_source = re.sub(r"\d+\.\d+\s*/\s*5\.0.*", "", current_source).strip()

    return events[:50]


# ---------------------------------------------------------------------------
# Additional history checks (page 2)
# ---------------------------------------------------------------------------

def _parse_additional_checks(page2: str) -> dict[str, str]:
    """Extract the per-owner check results from page 2."""
    checks: dict[str, str] = {}

    # Total Loss
    if "No total loss reported" in page2:
        checks["total_loss"] = "No Issues Reported"
    else:
        checks["total_loss"] = "Total loss reported"

    # Structural Damage
    if "CARFAX recommends that you have this vehicle inspected by a collision repair" in page2:
        checks["structural_damage"] = "Inspection recommended"
    elif "No Issues" in page2 and "Structural Damage" in page2:
        checks["structural_damage"] = "No Issues Reported"
    else:
        checks["structural_damage"] = "No Issues Reported"

    # Airbag Deployment
    if "No airbag deployment reported" in page2:
        checks["airbag_deployment"] = "No Issues Reported"
    else:
        checks["airbag_deployment"] = "No Issues Reported"

    # Odometer Check
    if "No indication of an odometer rollback" in page2:
        checks["odometer_check"] = "No Issues Indicated"
    else:
        checks["odometer_check"] = "No Issues Indicated"

    # Accident / Damage
    accident_match = re.search(r"Accident / Damage\s*(.*?)(?=Manufacturer Recall|Basic Warranty)", page2, re.S)
    if accident_match:
        section = accident_match.group(1)
        if "Accident reported" in section:
            date_match = re.search(r"Accident reported:\s*(\d{2}/\d{2}/\d{4})", section)
            date_str = date_match.group(1) if date_match else ""
            if "Minor Damage" in section:
                checks["accident_damage"] = f"Minor damage reported {date_str}"
            elif "Moderate" in section:
                checks["accident_damage"] = f"Moderate damage reported {date_str}"
            else:
                checks["accident_damage"] = f"Accident reported {date_str}"
        elif "No Issues" in section:
            checks["accident_damage"] = "No Issues Reported"
        else:
            checks["accident_damage"] = "No Issues Reported"
    else:
        checks["accident_damage"] = "No Issues Reported"

    # Manufacturer Recall
    if "No open recalls reported" in page2:
        checks["manufacturer_recall"] = "No Recalls Reported"
    else:
        checks["manufacturer_recall"] = "No Recalls Reported"

    # Basic Warranty
    if "Warranty Expired" in page2:
        checks["basic_warranty"] = "Warranty Expired"
    else:
        checks["basic_warranty"] = "Not Reported"

    # Theft / Stolen
    if "No theft" in page2 or "No stolen" in page2:
        checks["theft"] = "No Issues Reported"
    elif "Theft reported" in page2 or "Stolen" in page2:
        checks["theft"] = "Theft reported"
    else:
        checks["theft"] = "No Issues Reported"

    return checks


# ---------------------------------------------------------------------------
# Odometer
# ---------------------------------------------------------------------------

def _parse_odometer(full_text: str, page1: str) -> dict[str, Any]:
    """Extract odometer information."""
    result: dict[str, Any] = {}

    # Current mileage
    m = re.search(r"([\d,]+)\s*mi", page1)
    if m:
        result["current"] = m.group(1).replace(",", "")

    # Odometer rollback check
    if "No indication of an odometer rollback" in full_text:
        result["rollback_check"] = "No rollback detected"
    elif "odometer rollback" in full_text.lower():
        result["rollback_check"] = "Potential rollback detected"

    # Regular oil changes
    if "Regular Oil Changes" in full_text:
        result["regular_oil_changes"] = True

    return result


# ---------------------------------------------------------------------------
# Theft records
# ---------------------------------------------------------------------------

def _parse_theft_records(full_text: str) -> list[dict[str, Any]]:
    """Extract theft/stolen records from Carfax data."""
    records: list[dict[str, Any]] = []

    # Look for theft events in detailed history
    # Pattern: "MM/DD/YYYY Theft/Stolen vehicle reported"
    theft_patterns = [
        re.compile(r"(\d{2}/\d{2}/\d{4})\s*(?:Vehicle )?(?:reported )?(?:stolen|theft)", re.I),
        re.compile(r"(\d{2}/\d{2}/\d{4})\s*.*?(?:stolen|theft|larceny|carjacking)", re.I),
    ]

    for pattern in theft_patterns:
        for m in pattern.finditer(full_text):
            date = m.group(1)
            context = full_text[m.start():m.start() + 300]
            records.append({
                "date": date,
                "status": "Reported",
                "description": re.sub(r"\s+", " ", context[:200]).strip(),
            })

    # Deduplicate by date
    seen_dates: set[str] = set()
    unique: list[dict[str, Any]] = []
    for r in records:
        if r["date"] not in seen_dates:
            seen_dates.add(r["date"])
            unique.append(r)

    return unique


# ---------------------------------------------------------------------------
# Damage location
# ---------------------------------------------------------------------------

def _parse_damage_location(full_text: str) -> str:
    """Extract damage location if present."""
    if "Damage to front" in full_text or "front or side impact" in full_text.lower():
        return "Front"
    elif "Damage to rear" in full_text or "rear impact" in full_text.lower():
        return "Rear"
    elif "Damage to left" in full_text:
        return "Left"
    elif "Damage to right" in full_text:
        return "Right"
    return ""
