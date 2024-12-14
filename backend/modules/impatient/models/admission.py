from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text


class AdmissionBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    room_id: int = Field(foreign_key="room.id")

class Admission(AdmissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    staff_id: int = Field(foreign_key="staff.id")
    
    created_datetime: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_datetime: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ),
        default_factory=lambda: datetime.now(timezone.utc)
    )


class AdmissionCreate(AdmissionBase):
    ...
    

class AdmissionPublic(AdmissionBase):
    id: int
    staff_id: int
    created_datetime: datetime
    updated_datetime: datetime


class AdmissionUpdate(SQLModel):
    patient_id: int | None = None
    room_id: int | None = None
    staff_id: int | None = None