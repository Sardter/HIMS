from sqlmodel import select

from modules.patient.models.patient import Patient, PatientCreate, PatientUpdate, PatientStatus
from modules.database.session import SessionDep


def get_patient_all(
        *,
        session: SessionDep,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        gender: str | None = None,
        phone: str | None = None,
        status: PatientStatus | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Patient]:
    query = select(Patient).offset(offset).limit(limit)
    filters = [
        Patient.first_name.ilike(f"%{first_name}%") if first_name is not None else None,
        Patient.last_name.ilike(f"%{last_name}%") if last_name is not None else None,
        Patient.email.ilike(f"%{email}%") if email is not None else None,
        Patient.gender.ilike(f"%{gender}%") if gender is not None else None,
        Patient.phone.ilike(f"%{phone}%") if phone is not None else None,
        Patient.status == status if status is not None else None
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_patient_by_id( *, session: SessionDep, id: int) -> Patient | None:
    return session.get(Patient, id)


def create_patient( *, staff: PatientCreate, session: SessionDep) -> Patient | None:
    db_staff = Patient.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def update_patient(*, id: int, staff: PatientUpdate, session: SessionDep) -> Patient | None:
    db_staff = session.get(Patient, id)
    if not db_staff:
        return None
    staff_data = staff.model_dump(exclude_unset=True)
    db_staff.sqlmodel_update(staff_data)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_patient(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Patient, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True
