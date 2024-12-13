from sqlmodel import Field, SQLModel


class AdmissionBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    room_id: int = Field(foreign_key="room.id")
    staff_id: int = Field(foreign_key="staff.id")


class Admission(AdmissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AdmissionCreate(AdmissionBase):
    ...
    

class AdmissionPublic(AdmissionBase):
    id: int


class AdmissionUpdate(SQLModel):
    patient_id: int | None = None
    room_id: int | None = None
    staff_id: int | None = None