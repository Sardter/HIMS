from sqlmodel import Field, Relationship, SQLModel


class LogBase(SQLModel):
    staff_id: int = Field(foreign_key="staff.id")
    text: str = Field()


class Log(LogBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    

class LogCreate(LogBase):
    ...
    

class LogPublic(LogBase):
    id: int


class LogUpdate(SQLModel):
    staff_id: int | None = None
