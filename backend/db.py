import os
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to backend/.env "
        "(e.g. postgresql+psycopg2://user:password@localhost:5432/vin_report)."
    )

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5)


def get_session():
    with Session(engine) as session:
        yield session
