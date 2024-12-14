from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text

class NoteBase(SQLModel):
    text: str = Field()
    
    admission_id: int = Field(foreign_key="admission.id")


class Note(NoteBase, table=True):
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
    

class NoteCreate(NoteBase):
    ...
    

class NotePublic(NoteBase):
    id: int
    staff_id: int
    created_datetime: datetime
    updated_datetime: datetime


class NoteUpdate(SQLModel):
    text: str | None = None
