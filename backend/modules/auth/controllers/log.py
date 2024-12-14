from sqlmodel import select
from datetime import datetime

from modules.auth.models.log import Log, LogCreate
from modules.database.session import SessionDep


def get_log_all(
        *,
        session: SessionDep,
        text: str | None = None,
        staff_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
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
    ) -> list[Log]:
    query = select(Log).offset(offset).limit(limit)
    filters = [
        Log.staff_id == staff_id if staff_id is not None else None,
        Log.text.ilike(f"%{text}%") if text is not None else None,
        Log.created_datetime == created_datetime if created_datetime is not None else None,
        Log.created_datetime > created_datetime__gt if created_datetime__gt is not None else None,
        Log.created_datetime < created_datetime__lt if created_datetime__lt is not None else None,
        Log.created_datetime >= created_datetime__gte if created_datetime__gte is not None else None,
        Log.created_datetime <= created_datetime__lte if created_datetime__lte is not None else None,
        Log.updated_datetime == updated_datetime if updated_datetime is not None else None,
        Log.updated_datetime > updated_datetime__gt if updated_datetime__gt is not None else None,
        Log.updated_datetime < updated_datetime__lt if updated_datetime__lt is not None else None,
        Log.updated_datetime >= updated_datetime__gte if updated_datetime__gte is not None else None,
        Log.updated_datetime <= updated_datetime__lte if updated_datetime__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_log_by_id(*, session: SessionDep, id: int) -> Log | None:
    return session.get(Log, id)


def create_log( *, staff: LogCreate, session: SessionDep) -> Log | None:
    db_staff = Log.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_log(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Log, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True
