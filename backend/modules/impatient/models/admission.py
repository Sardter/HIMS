import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text


class AdmissionBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    room_id: int = Field(foreign_key="room.id")
    staff_id: int = Field(foreign_key="staff.id")


class Admission(AdmissionBase, table=True):
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


class AdmissionCreate(AdmissionBase):
    ...
    

class AdmissionPublic(AdmissionBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime


class AdmissionUpdate(SQLModel):
    patient_id: int | None = None
    room_id: int | None = None
    staff_id: int | None = None