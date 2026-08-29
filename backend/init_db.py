from sqlalchemy import text
from sqlmodel import SQLModel

from db import engine
import models  # noqa: F401 — registers tables

COMPOSITE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_tsbs_make_model_norm ON tsbs (make, model_norm)",
    "CREATE INDEX IF NOT EXISTS ix_tsbs_make_model_norm_year ON tsbs (make, model_norm, model_year)",
    "CREATE INDEX IF NOT EXISTS ix_inv_make_model_norm ON investigations (make, model_norm)",
]


def ensure_indexes() -> None:
    with engine.begin() as conn:
        for statement in COMPOSITE_INDEXES:
            conn.execute(text(statement))
    print("Composite indexes ensured.")


def main() -> None:
    SQLModel.metadata.create_all(engine)
    print("Tables created:", sorted(SQLModel.metadata.tables.keys()))
    ensure_indexes()


if __name__ == "__main__":
    main()
