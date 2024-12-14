import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text
from enum import Enum


class PatientStatus(Enum):
    Registered = 1
    Admitted = 2
    Discharged = 3


class PatientBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    gender: str = Field()
    email: str | None = Field(default=None, index=True)
    phone: str | None = Field(default=None, index=True)
    status: PatientStatus = Field(default=PatientStatus.Registered)
    

class Patient(PatientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_datetime: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    

class PatientCreate(PatientBase):
    ...


class PatientPublic(PatientBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime


class PatientUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    email: str | None = None
    phone: str | None = None
    status: PatientStatus | None = None