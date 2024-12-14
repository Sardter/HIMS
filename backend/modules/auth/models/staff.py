from datetime import datetime
from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text


class StaffBase(SQLModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    phone: str | None = Field(default=None, index=True)


class Staff(StaffBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
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
    

class StaffCreate(StaffBase):
    password: str
    

class StaffPublic(StaffBase):
    id: int
    created_datetime: datetime
    updated_datetime: datetime


class StaffUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str | None = None
    phone: str | None = None
    password: str | None = None


class StaffLogin(SQLModel):
    username: str
    passowrd: str