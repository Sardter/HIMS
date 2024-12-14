from sqlmodel import select

from modules.auth.models.log import Log, LogCreate
from modules.database.session import SessionDep


def get_log_all(
        *,
        session: SessionDep,
        text: str | None = None,
        staff_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Log]:
    query = select(Log).offset(offset).limit(limit)
    filters = [
        Log.staff_id == staff_id if staff_id is not None else None,
        Log.text.ilike(f"%{text}%") if text is not None else None,
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
