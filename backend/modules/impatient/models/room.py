from datetime import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text

class RoomBase(SQLModel):
    name: str = Field(index=True)
    maximum_capacity: int = Field(default=0)


class Room(RoomBase, table=True):
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


class RoomCreate(RoomBase):
    ...
    

class RoomPublic(RoomBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime


class RoomUpdate(SQLModel):
    name: str | None = None
    maximum_capacity: int | None = None
