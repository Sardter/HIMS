from sqlmodel import select

from modules.impatient.models.room import Room, RoomCreate, RoomUpdate
from modules.database.session import SessionDep


def get_room_all(
        *,
        session: SessionDep,
        name: str | None = None,
        maximum_capacity: int | None = None,
        maximum_capacity__gt: int | None = None,
        maximum_capacity__lt: int | None = None,
        maximum_capacity__gte: int | None = None,
        maximum_capacity__lte: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Room]:
    query = select(Room).offset(offset).limit(limit)
    filters = [
        Room.name.ilike(f"%{name}%") if name is not None else None,
        Room.maximum_capacity == maximum_capacity if maximum_capacity is not None else None,
        Room.maximum_capacity > maximum_capacity__gt if maximum_capacity__gt is not None else None,
        Room.maximum_capacity < maximum_capacity__lt if maximum_capacity__lt is not None else None,
        Room.maximum_capacity >= maximum_capacity__gte if maximum_capacity__gte is not None else None,
        Room.maximum_capacity <= maximum_capacity__lte if maximum_capacity__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_room_by_id( *, session: SessionDep, id: int) -> Room | None:
    return session.get(Room, id)


def create_room( *, staff: RoomCreate, session: SessionDep) -> Room | None:
    db_staff = Room.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def update_room(*, id: int, staff: RoomUpdate, session: SessionDep) -> Room | None:
    db_staff = session.get(Room, id)
    if not db_staff:
        return None
    staff_data = staff.model_dump(exclude_unset=True)
    db_staff.sqlmodel_update(staff_data)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_room(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Room, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True
