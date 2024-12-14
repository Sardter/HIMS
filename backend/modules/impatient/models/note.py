from datetime import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text

class NoteBase(SQLModel):
    text: str = Field()
    
    admission_id: int = Field(foreign_key="admission.id")
    staff_id: int = Field(foreign_key="staff.id")


class Note(NoteBase, table=True):
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
    

class NoteCreate(NoteBase):
    ...
    

class NotePublic(NoteBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime


class NoteUpdate(SQLModel):
    text: str | None = None
