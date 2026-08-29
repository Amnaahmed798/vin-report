import csv
import sys
from pathlib import Path

from sqlmodel import Session, select

from db import engine
from models import SafetyRating

RAW_FILE = Path(__file__).parent / "data" / "raw" / "safety_ratings" / "safercar.csv"

COLUMNS = {
    "make": "MAKE",
    "model": "MODEL",
    "model_year": "MODEL_YR",
    "body_style": "BODY_STYLE",
    "vehicle_type": "VEHICLE_TYPE",
    "drive_train": "DRIVE_TRAIN",
    "overall_stars": "OVERALL_STARS",
    "overall_frnt_stars": "OVERALL_FRNT_STARS",
    "overall_side_stars": "OVERALL_SIDE_STARS",
    "rollover_stars": "ROLLOVER_STARS",
    "frnt_vin": "FRNT_VIN",
    "side_vin": "SIDE_VIN",
    "pole_vin": "POLE_VIN",
}


def clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def main() -> None:
    if not RAW_FILE.exists():
        print("Missing", RAW_FILE)
        sys.exit(1)

    with Session(engine) as session:
        existing = session.exec(select(SafetyRating).limit(1)).first()
        if existing is not None:
            print("Table already has data — truncating...")
            session.exec(  # type: ignore[attr-defined]
                SafetyRating.__table__.delete()
            )
            session.commit()

    batch: list[SafetyRating] = []
    count = 0
    batch_size = 5000
    with Session(engine) as session:
        with open(RAW_FILE, encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kwargs = {field: clean(row.get(col)) for field, col in COLUMNS.items()}
                batch.append(SafetyRating(**kwargs))
                if len(batch) >= batch_size:
                    session.add_all(batch)
                    session.commit()
                    count += len(batch)
                    batch = []
        if batch:
            session.add_all(batch)
            session.commit()
            count += len(batch)
    print(f"Imported {count:,} safety ratings")


if __name__ == "__main__":
    main()
