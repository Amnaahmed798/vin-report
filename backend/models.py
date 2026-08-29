from datetime import date

from sqlalchemy import Index
from sqlmodel import Field, SQLModel


class Tsb(SQLModel, table=True):
    __tablename__ = "tsbs"
    __table_args__ = (
        Index("ix_tsbs_make_model_norm", "make", "model_norm"),
        Index("ix_tsbs_make_model_norm_year", "make", "model_norm", "model_year"),
    )

    id: int | None = Field(default=None, primary_key=True)
    doc_id: str = Field(index=True, max_length=128)
    make: str = Field(index=True, max_length=128)
    model: str = Field(index=True, max_length=256)
    model_norm: str = Field(index=True, max_length=256)
    model_year: str = Field(index=True, max_length=512)
    summary: str | None = Field(default=None, max_length=4000)
    source_file: str | None = Field(default=None, max_length=64)


class Investigation(SQLModel, table=True):
    __tablename__ = "investigations"
    __table_args__ = (
        Index("ix_inv_make_model_norm", "make", "model_norm"),
    )

    id: int | None = Field(default=None, primary_key=True)
    action_no: str = Field(index=True, max_length=10)
    make: str = Field(index=True, max_length=25)
    model: str = Field(index=True, max_length=256)
    model_norm: str = Field(index=True, max_length=256)
    year: str = Field(index=True, max_length=4)
    component: str | None = Field(default=None, max_length=256)
    mfr_name: str | None = Field(default=None, max_length=40)
    date_opened: date | None = None
    date_closed: date | None = None
    campno: str | None = Field(default=None, max_length=9)
    subject: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=6000)


class SafetyRating(SQLModel, table=True):
    __tablename__ = "safety_ratings"

    id: int | None = Field(default=None, primary_key=True)
    make: str = Field(index=True, max_length=128)
    model: str = Field(index=True, max_length=256)
    model_year: str = Field(index=True, max_length=4)
    body_style: str | None = None
    vehicle_type: str | None = None
    drive_train: str | None = None
    overall_stars: str | None = None
    overall_frnt_stars: str | None = None
    overall_side_stars: str | None = None
    rollover_stars: str | None = None
    frnt_vin: str | None = None
    side_vin: str | None = None
    pole_vin: str | None = None
