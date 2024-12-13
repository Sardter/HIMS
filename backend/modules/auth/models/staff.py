from sqlmodel import Field, Relationship, SQLModel

from modules.impatient.models.admission import Admission


class StaffBase(SQLModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str = Field(index=True)
    username: str = Field(index=True)
    phone: str | None = Field(default=None, index=True)


class Staff(StaffBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_passord: str = Field()
    
    admissions: list[Admission] = Relationship(back_populates="staff")
    
    @staticmethod
    def foreign_key_descriptor() -> str:
        return "staff.id"
    

class StaffCreate(StaffBase):
    password: str
    

class StaffPublic(StaffBase):
    id: int


class StaffUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str | None = None
    phone: str | None = None
    password: str | None = None