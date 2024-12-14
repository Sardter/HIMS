import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text


class LogBase(SQLModel):
    staff_id: int = Field(foreign_key="staff.id")
    text: str = Field()


class Log(LogBase, table=True):
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
    

class LogCreate(LogBase):
    ...
    

class LogPublic(LogBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime
