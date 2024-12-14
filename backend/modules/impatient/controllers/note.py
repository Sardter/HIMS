from sqlmodel import select
from datetime import datetime

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
    ) -> list[Note]:
    query = select(Note).offset(offset).limit(limit)
    filters = [
        Note.admission_id == admission_id if admission_id is not None else None,
        Note.staff_id == staff_id if staff_id is not None else None,
        Note.text.ilike(f"%{text}%") if text is not None else None,
        Note.created_datetime == created_datetime if created_datetime is not None else None,
        Note.created_datetime > created_datetime__gt if created_datetime__gt is not None else None,
        Note.created_datetime < created_datetime__lt if created_datetime__lt is not None else None,
        Note.created_datetime >= created_datetime__gte if created_datetime__gte is not None else None,
        Note.created_datetime <= created_datetime__lte if created_datetime__lte is not None else None,
        Note.updated_datetime == updated_datetime if updated_datetime is not None else None,
        Note.updated_datetime > updated_datetime__gt if updated_datetime__gt is not None else None,
        Note.updated_datetime < updated_datetime__lt if updated_datetime__lt is not None else None,
        Note.updated_datetime >= updated_datetime__gte if updated_datetime__gte is not None else None,
        Note.updated_datetime <= updated_datetime__lte if updated_datetime__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_note_by_id( *, session: SessionDep, id: int) -> Note | None:
    return session.get(Note, id)


def create_note( *, staff_id: int, note: NoteCreate, session: SessionDep) -> Note | None:
    db_note = Note.model_validate(note, update={'staff_id': staff_id})
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


def update_note(*, id: int, note: NoteUpdate, session: SessionDep) -> Note | None:
    db_note = session.get(Note, id)
    if not db_note:
        return None
    note_data = note.model_dump(exclude_unset=True)
    db_note.sqlmodel_update(note_data)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


def delete_note(*, id: int, session: SessionDep) -> bool:
    db_note = session.get(Note, id)
    if db_note is None:
        return False
    session.delete(db_note)
    session.commit()
    return True
