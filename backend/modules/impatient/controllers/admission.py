from sqlmodel import select
from datetime import datetime

from modules.impatient.models.admission import Admission, AdmissionCreate, AdmissionUpdate
from modules.database.session import SessionDep
from modules.impatient.models.note import Note
from modules.impatient.models.room import Room
from modules.impatient.controllers.room import get_room_by_id
from modules.patient.controllers.patient import get_patient_by_id, update_patient
from modules.patient.models.patient import Patient, PatientStatus, PatientUpdate
from modules.impatient.controllers.exceptions import RoomCapacityOverFlow, RoomDoesNotExist, PatientDoesNotExist, PatientAlreadyInRoom

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


def create_admission( *, staff_id: int, admission: AdmissionCreate, session: SessionDep) -> Admission | None:
    room = get_room_by_id(session=session, id=admission.room_id)
    if room is None:
        raise RoomDoesNotExist
    patient = get_patient_by_id(session=session, id=admission.patient_id)
    if patient is None:
        raise PatientDoesNotExist
    
    patient_in_room_query = select(Patient, Admission, Room).where(
        Patient.id == admission.patient_id, 
        Room.id == room.id
    )
    
    patient_is_in_room = session.exec(patient_in_room_query).all()
    
    if patient_is_in_room:
        raise PatientAlreadyInRoom
    
    patient_count_query = select(Patient, Admission, Room).where(
        Patient.id == Admission.patient_id, 
        Room.id == room.id, 
        Patient.status == PatientStatus.Admitted
    )
    patient_count = len(session.exec(patient_count_query).all())
    if patient_count + 1 > room.maximum_capacity:
        raise RoomCapacityOverFlow
    
    update_patient(id=patient.id, session=session, patient=PatientUpdate(status=PatientStatus.Admitted))
    
    db_admission = Admission.model_validate(admission, update={'staff_id': staff_id})
    session.add(db_admission)
    session.commit()
    session.refresh(db_admission)
    return db_admission


def get_admission_notes(
        *, id: int, 
        session: SessionDep,
        offset: int | None = None,
        limit: int | None = None) -> list[Note] | None:
    
    db_admission = session.get(Admission, id)
    if not db_admission:
        return None
    query = select(Note).where(Note.admission_id == db_admission.id).offset(offset).limit(limit)

    return session.exec(query).all()


def update_admission(*, id: int, admission: AdmissionUpdate, session: SessionDep) -> Admission | None:
    db_admission = session.get(Admission, id)
    if not db_admission:
        return None
    staff_data = admission.model_dump(exclude_unset=True)
    db_admission.sqlmodel_update(staff_data)
    session.add(db_admission)
    session.commit()
    session.refresh(db_admission)
    return db_admission


def delete_admission(*, id: int, session: SessionDep) -> bool:
    db_admission = session.get(Admission, id)
    if db_admission is None:
        return False
    
    update_patient(id=db_admission.patient_id, session=session, patient=PatientUpdate(status=PatientStatus.Discharged))
    
    session.delete(db_admission)
    session.commit()
    return True
