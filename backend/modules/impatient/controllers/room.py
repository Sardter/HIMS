from sqlmodel import select
from datetime import datetime

from modules.impatient.models.room import Room, RoomCreate, RoomUpdate
from modules.database.session import SessionDep
from modules.impatient.models.admission import Admission


def get_room_all(
        *,
        session: SessionDep,
        name: str | None = None,
        maximum_capacity: int | None = None,
        maximum_capacity__gt: int | None = None,
        maximum_capacity__lt: int | None = None,
        maximum_capacity__gte: int | None = None,
        maximum_capacity__lte: int | None = None,
        created_datetime: datetime | None = None,
        created_datetime__gt: datetime | None = None,
        created_datetime__lt: datetime | None = None,
        created_datetime__gte: datetime | None = None,
        created_datetime__lte: datetime | None = None,
        updated_datetime: datetime | None = None,
        updated_datetime__gt: datetime | None = None,
        updated_datetime__lt: datetime | None = None,
        updated_datetime__gte: datetime | None = None,
        updated_datetime__lte: datetime | None = None,
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
        Room.created_datetime == created_datetime if created_datetime is not None else None,
        Room.created_datetime > created_datetime__gt if created_datetime__gt is not None else None,
        Room.created_datetime < created_datetime__lt if created_datetime__lt is not None else None,
        Room.created_datetime >= created_datetime__gte if created_datetime__gte is not None else None,
        Room.created_datetime <= created_datetime__lte if created_datetime__lte is not None else None,
        Room.updated_datetime == updated_datetime if updated_datetime is not None else None,
        Room.updated_datetime > updated_datetime__gt if updated_datetime__gt is not None else None,
        Room.updated_datetime < updated_datetime__lt if updated_datetime__lt is not None else None,
        Room.updated_datetime >= updated_datetime__gte if updated_datetime__gte is not None else None,
        Room.updated_datetime <= updated_datetime__lte if updated_datetime__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_room_by_id( *, session: SessionDep, id: int) -> Room | None:
    return session.get(Room, id)


def get_room_admissions(
        *, id: int, 
        session: SessionDep,
        offset: int | None = None,
        limit: int | None = None) -> list[Admission] | None:
    
    db_staff = session.get(Room, id)
    if not db_staff:
        return None
    query = select(Admission).where(Admission.room_id == db_staff.id).offset(offset).limit(limit)

    return session.exec(query).all()


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
