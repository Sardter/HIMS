from sqlmodel import select

from modules.impatient.models.note import Note, NoteCreate, NoteUpdate
from modules.database.session import SessionDep


def get_note_all(
        *,
        session: SessionDep,
        text: str | None = None,
        admission_id: int | None = None,
        staff_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Note]:
    query = select(Note).offset(offset).limit(limit)
    filters = [
        Note.admission_id == admission_id if admission_id is not None else None,
        Note.staff_id == staff_id if staff_id is not None else None,
        Note.text.ilike(f"%{text}%") if text is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_note_by_id( *, session: SessionDep, id: int) -> Note | None:
    return session.get(Note, id)


def create_note( *, staff: NoteCreate, session: SessionDep) -> Note | None:
    db_staff = Note.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def update_note(*, id: int, staff: NoteUpdate, session: SessionDep) -> Note | None:
    db_staff = session.get(Note, id)
    if not db_staff:
        return None
    staff_data = staff.model_dump(exclude_unset=True)
    db_staff.sqlmodel_update(staff_data)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_note(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Note, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True
