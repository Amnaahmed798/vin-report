"""Scheduled refresh job: re-download bulk datasets and re-import into DB.

Cross-platform (Windows / Linux), uses only the Python standard library.

Run manually from the backend directory:
    .venv\\Scripts\\python.exe refresh_bulk.py        (Windows)
    .venv/bin/python refresh_bulk.py                 (Linux)

Or schedule it (run inside the backend directory):
  Windows Task Scheduler:
      schtasks /Create /SC WEEKLY /D MON /ST 03:00 /TN "VIN-BulkRefresh" /TR "C:\\path\\to\\backend\\.venv\\Scripts\\python.exe C:\\path\\to\\backend\\refresh_bulk.py"
  Linux cron:
      0 3 * * 1  cd /path/to/backend && .venv/bin/python refresh_bulk.py >> logs/refresh.log 2>&1

Output is appended to logs/refresh.log automatically.
"""

import io
import sys
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw"
LOG = BASE / "logs"

TSB_ZIPS = [
    "https://static.nhtsa.gov/odi/ffdd/tsbs/MFR_COMMS_RECEIVED_{}.zip".format(y)
    for y in ["1995-1999", "2000-2004", "2005-2009", "2010-2014", "2015-2019",
              "2020-2024", "2025-2025", "2026-2026"]
]
INV_ZIP = "https://static.nhtsa.gov/odi/ffdd/inv/FLAT_INV.zip"
SAFETY_CSV = "https://static.nhtsa.gov/nhtsa/downloads/Safercar/Safercar_data.csv"


def log(message: str) -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}"
    print(line)
    LOG.mkdir(parents=True, exist_ok=True)
    with open(LOG / "refresh.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=600) as resp:
            data = resp.read()
    except Exception as exc:
        log(f"! failed to download {url}: {exc}")
        return False
    dest.write_bytes(data)
    log(f"+ downloaded {dest.name} ({len(data):,} bytes)")
    return True


def extract_zip(zip_path: Path, dest_dir: Path) -> bool:
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
    except (zipfile.BadZipFile, OSError) as exc:
        log(f"! {zip_path.name} is not a valid zip (NHTSA may not publish this range yet): {exc}")
        zip_path.unlink(missing_ok=True)
        return False
    log(f"+ extracted {zip_path.name} -> {dest_dir.name}")
    return True


def main() -> None:
    tsb_dir = RAW / "tsbs"
    for url in TSB_ZIPS:
        name = url.rsplit("/", 1)[-1]
        dest = tsb_dir / name
        if download(url, dest):
            extract_zip(dest, tsb_dir)

    inv_dir = RAW / "investigations"
    inv_zip = inv_dir / "FLAT_INV.zip"
    if download(INV_ZIP, inv_zip):
        extract_zip(inv_zip, inv_dir)

    safety_dir = RAW / "safety_ratings"
    download(SAFETY_CSV, safety_dir / "safercar.csv")

    python = sys.executable
    for script in ["import_tsbs.py", "import_inv.py", "import_safety.py"]:
        log(f"+ running {script}")
        subprocess_result(script, python)

    log("Refresh complete.")


def subprocess_result(script: str, python: str) -> None:
    import subprocess
    result = subprocess.run([python, script], cwd=BASE, capture_output=True, text=True)
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0:
        log(f"! {script} exited with code {result.returncode}: {result.stderr.strip()}")


if __name__ == "__main__":
    main()
