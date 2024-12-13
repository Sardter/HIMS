from sqlmodel import Field, Relationship, SQLModel

from modules.impatient.models.room import Room
from modules.patient.models.patient import Patient
from modules.auth.models.staff import Staff

from modules.impatient.models.note import Note

class AdmissionBase(SQLModel):
    patient_id: int = Field(foreign_key=Patient.foreign_key_descriptor())
    room_id: int = Field(foreign_key=Room.foreign_key_descriptor())
    staff_id: int = Field(foreign_key=Staff.foreign_key_descriptor())


class Admission(AdmissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    patient: Patient = Relationship(back_populates="admissions")
    room: Room = Relationship(back_populates="admissions")
    staff: Staff = Relationship(back_populates="admissions")
    
    notes: list[Note] = Relationship(back_populates="admission")
    
    @staticmethod
    def foreign_key_descriptor() -> str:
        return "room.id"
    

class AdmissionCreate(AdmissionBase):
    ...
    

class AdmissionPublic(AdmissionBase):
    id: int


class AdmissionUpdate(SQLModel):
    patient_id: int | None = None
    room_id: int | None = None
    staff_id: int | None = None