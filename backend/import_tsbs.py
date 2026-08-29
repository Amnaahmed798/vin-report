import csv
import re
import sys
from pathlib import Path

from sqlmodel import Session, select

from db import engine
from models import Tsb

RAW_DIR = Path(__file__).parent / "data" / "raw" / "tsbs"


def norm_model(model: str) -> str:
    return re.sub(r"\s+", "", model.upper())


def import_file(path: Path) -> tuple[int, int]:
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows: list[Tsb] = []
        count = 0
        batch_size = 5000
        with Session(engine) as session:
            for row in reader:
                if len(row) < 5:
                    continue
                rows.append(
                    Tsb(
                        doc_id=row[0].strip(),
                        make=row[1].strip(),
                        model=row[2].strip(),
                        model_norm=norm_model(row[2]),
                        model_year=row[3].strip(),
                        summary=row[4].strip() or None,
                        source_file=path.name,
                    )
                )
                if len(rows) >= batch_size:
                    session.add_all(rows)
                    session.commit()
                    count += len(rows)
                    rows = []
            if rows:
                session.add_all(rows)
                session.commit()
                count += len(rows)
    return count


def main() -> None:
    files = sorted(RAW_DIR.glob("MFR_COMMS_RECEIVED_*.csv"))
    if not files:
        print("No TSB CSV files found in", RAW_DIR)
        sys.exit(1)

    with Session(engine) as session:
        existing = session.exec(select(Tsb).limit(1)).first()
        if existing is not None:
            print("Table already has data — truncating...")
            session.exec(  # type: ignore[attr-defined]
                Tsb.__table__.delete()
            )
            session.commit()

    total = 0
    for f in files:
        n = import_file(f)
        total += n
        print(f"Imported {n:,} rows from {f.name}")
    print(f"Total TSB rows: {total:,}")


if __name__ == "__main__":
    main()
