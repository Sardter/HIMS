from sqlmodel import select

from modules.impatient.models.admission import Admission, AdmissionCreate, AdmissionUpdate
from modules.database.session import SessionDep


def get_admission_all(
        *,
        session: SessionDep,
        patient_id: int | None = None,
        room_id: int | None = None,
        staff_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Admission]:
    query = select(Admission).offset(offset).limit(limit)
    filters = [
        Admission.patient_id == patient_id if patient_id is not None else None,
        Admission.room_id == room_id if room_id is not None else None,
        Admission.staff_id == staff_id if staff_id is not None else None,
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
