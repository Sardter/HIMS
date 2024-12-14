from sqlmodel import select
from datetime import datetime

from modules.impatient.models.admission import Admission, AdmissionCreate, AdmissionUpdate
from modules.database.session import SessionDep
from modules.impatient.models.note import Note

def get_admission_all(
        *,
        session: SessionDep,
        patient_id: int | None = None,
        room_id: int | None = None,
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
    ) -> list[Admission]:
    query = select(Admission).offset(offset).limit(limit)
    filters = [
        Admission.patient_id == patient_id if patient_id is not None else None,
        Admission.room_id == room_id if room_id is not None else None,
        Admission.staff_id == staff_id if staff_id is not None else None,
        Admission.created_datetime == created_datetime if created_datetime is not None else None,
        Admission.created_datetime > created_datetime__gt if created_datetime__gt is not None else None,
        Admission.created_datetime < created_datetime__lt if created_datetime__lt is not None else None,
        Admission.created_datetime >= created_datetime__gte if created_datetime__gte is not None else None,
        Admission.created_datetime <= created_datetime__lte if created_datetime__lte is not None else None,
        Admission.updated_datetime == updated_datetime if updated_datetime is not None else None,
        Admission.updated_datetime > updated_datetime__gt if updated_datetime__gt is not None else None,
        Admission.updated_datetime < updated_datetime__lt if updated_datetime__lt is not None else None,
        Admission.updated_datetime >= updated_datetime__gte if updated_datetime__gte is not None else None,
        Admission.updated_datetime <= updated_datetime__lte if updated_datetime__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_admission_by_id( *, session: SessionDep, id: int) -> Admission | None:
    return session.get(Admission, id)


def create_admission( *, staff: AdmissionCreate, session: SessionDep) -> Admission | None:
    db_staff = Admission.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def get_admission_notes(
        *, id: int, 
        session: SessionDep,
        offset: int | None = None,
        limit: int | None = None) -> list[Note] | None:
    
    db_staff = session.get(Admission, id)
    if not db_staff:
        return None
    query = select(Note).where(Note.admission_id == db_staff.id).offset(offset).limit(limit)

    return session.exec(query).all()


def update_admission(*, id: int, staff: AdmissionUpdate, session: SessionDep) -> Admission | None:
    db_staff = session.get(Admission, id)
    if not db_staff:
        return None
    staff_data = staff.model_dump(exclude_unset=True)
    db_staff.sqlmodel_update(staff_data)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_admission(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Admission, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True
