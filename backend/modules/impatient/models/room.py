from sqlmodel import Field, Relationship, SQLModel

from modules.impatient.models.admission import Admission

class RoomBase(SQLModel):
    name: str = Field(index=True)
    maximum_capacity: int = Field(default=0)


class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    admissions: list[Admission] = Relationship(back_populates="room")
    
    @staticmethod
    def foreign_key_descriptor() -> str:
        return "room.id"
    

class RoomCreate(RoomBase):
    ...
    

class RoomPublic(RoomBase):
    id: int


class RoomUpdate(SQLModel):
    name: str | None = None
    maximum_capacity: int | None = None
