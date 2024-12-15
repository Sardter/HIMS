from sqlmodel import select
from datetime import datetime

from modules.patient.models.patient import Patient, PatientCreate, PatientUpdate, PatientStatus
from modules.database.session import SessionDep
from modules.impatient.models.admission import Admission
import requests



def get_patient_all(
        *,
        session: SessionDep,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        gender: str | None = None,
        phone: str | None = None,
        status: PatientStatus | None = None,
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
    ) -> list[Patient]:
    query = select(Patient).offset(offset).limit(limit)
    filters = [
        Patient.first_name.ilike(f"%{first_name}%") if first_name is not None else None,
        Patient.last_name.ilike(f"%{last_name}%") if last_name is not None else None,
        Patient.email.ilike(f"%{email}%") if email is not None else None,
        Patient.gender.ilike(f"%{gender}%") if gender is not None else None,
        Patient.phone.ilike(f"%{phone}%") if phone is not None else None,
        Patient.status == status if status is not None else None,
        Patient.created_datetime == created_datetime if created_datetime is not None else None,
        Patient.created_datetime > created_datetime__gt if created_datetime__gt is not None else None,
        Patient.created_datetime < created_datetime__lt if created_datetime__lt is not None else None,
        Patient.created_datetime >= created_datetime__gte if created_datetime__gte is not None else None,
        Patient.created_datetime <= created_datetime__lte if created_datetime__lte is not None else None,
        Patient.updated_datetime == updated_datetime if updated_datetime is not None else None,
        Patient.updated_datetime > updated_datetime__gt if updated_datetime__gt is not None else None,
        Patient.updated_datetime < updated_datetime__lt if updated_datetime__lt is not None else None,
        Patient.updated_datetime >= updated_datetime__gte if updated_datetime__gte is not None else None,
        Patient.updated_datetime <= updated_datetime__lte if updated_datetime__lte is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_patient_by_id( *, session: SessionDep, id: int) -> Patient | None:
    return session.get(Patient, id)


def create_patient( *, patient: PatientCreate, session: SessionDep) -> Patient | None:
    db_patient = Patient.model_validate(patient)
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient


def get_patient_admissions(
        *, id: int, 
        session: SessionDep,
        offset: int | None = None,
        limit: int | None = None) -> list[Admission] | None:
    
    db_patient = session.get(Patient, id)
    if not db_patient:
        return None
    query = select(Admission).where(Admission.patient_id == db_patient.id).offset(offset).limit(limit)

    return session.exec(query).all()


def update_patient(*, id: int, patient: PatientUpdate, session: SessionDep) -> Patient | None:
    db_patient = session.get(Patient, id)
    if not db_patient:
        return None
    staff_data = patient.model_dump(exclude_unset=True)
    db_patient.sqlmodel_update(staff_data)
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient


def delete_patient(*, patient_id: int, session: SessionDep) -> bool:
    """Delete a patient record using session."""
    db_patient = session.get(Patient, patient_id)
    if not db_patient:
        return False  # Patient not found, cannot delete

    session.delete(db_patient)
    session.commit()
    return True  # Successfully deleted the patient