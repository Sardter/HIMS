from sqlmodel import Field, Relationship, SQLModel

from modules.impatient.models.admission import Admission

class NoteBase(SQLModel):
    text: str = Field()
    
    admission_id: int = Field(foreign_key=Admission.foreign_key_descriptor())


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    admission: Admission = Relationship(back_populates="notes")  
    

class NoteCreate(NoteBase):
    ...
    

class NotePublic(NoteBase):
    id: int


class NoteUpdate(SQLModel):
    text: str | None = None
