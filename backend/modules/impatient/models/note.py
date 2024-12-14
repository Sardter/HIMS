from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    text: str = Field()
    
    admission_id: int = Field(foreign_key="admission.id")
    staff_id: int = Field(foreign_key="staff.id")


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    

class NoteCreate(NoteBase):
    ...
    

class NotePublic(NoteBase):
    id: int


class NoteUpdate(SQLModel):
    text: str | None = None
