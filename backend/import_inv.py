import sys
from datetime import date, datetime
from pathlib import Path
import re

from sqlmodel import Session, select

from db import engine
from models import Investigation

RAW_FILE = Path(__file__).parent / "data" / "raw" / "investigations" / "FLAT_INV.txt"

DATE_FMT = "%Y%m%d"


def norm_model(model: str) -> str:
    return re.sub(r"\s+", "", model.upper())


def parse_date(value: str) -> date | None:
    value = value.strip()
    if len(value) != 8 or not value.isdigit() or value == "00000000":
        return None
    try:
        return datetime.strptime(value, DATE_FMT).date()
    except ValueError:
        return None


def main() -> None:
    if not RAW_FILE.exists():
        print("Missing", RAW_FILE)
        sys.exit(1)

    with Session(engine) as session:
        existing = session.exec(select(Investigation).limit(1)).first()
        if existing is not None:
            print("Table already has data — truncating...")
            session.exec(  # type: ignore[attr-defined]
                Investigation.__table__.delete()
            )
            session.commit()

    batch: list[Investigation] = []
    count = 0
    batch_size = 5000
    with Session(engine) as session:
        with open(RAW_FILE, encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 11:
                    continue
                batch.append(
                    Investigation(
                        action_no=parts[0].strip(),
                        make=parts[1].strip(),
                        model=parts[2].strip(),
                        model_norm=norm_model(parts[2]),
                        year=parts[3].strip(),
                        component=parts[4].strip() or None,
                        mfr_name=parts[5].strip() or None,
                        date_opened=parse_date(parts[6]),
                        date_closed=parse_date(parts[7]),
                        campno=parts[8].strip() or None,
                        subject=parts[9].strip() or None,
                        summary=parts[10].strip() or None,
                    )
                )
                if len(batch) >= batch_size:
                    session.add_all(batch)
                    session.commit()
                    count += len(batch)
                    batch = []
        if batch:
            session.add_all(batch)
            session.commit()
            count += len(batch)
    print(f"Imported {count:,} investigations")


if __name__ == "__main__":
    main()
