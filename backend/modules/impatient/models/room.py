from sqlmodel import Field, SQLModel

class RoomBase(SQLModel):
    name: str = Field(index=True)
    maximum_capacity: int = Field(default=0)


class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class RoomCreate(RoomBase):
    ...
    

class RoomPublic(RoomBase):
    id: int


class RoomUpdate(SQLModel):
    name: str | None = None
    maximum_capacity: int | None = None
