from sqlmodel import Field, Relationship, SQLModel

from modules.auth.models.staff import Staff

class LogBase(SQLModel):
    staff_id: int = Field(foreign_key=Staff.foreign_key_descriptor())
    text: str = Field()


class Log(LogBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    staff: Staff = Relationship(back_populates="logs")
    

class LogCreate(LogBase):
    ...
    

class LogPublic(LogBase):
    id: int


class LogUpdate(SQLModel):
    staff_id: int | None = None
