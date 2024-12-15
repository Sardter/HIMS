from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.patient.controllers.patient import get_patient_all, get_patient_by_id, create_patient, update_patient, delete_patient, get_patient_admissions
from modules.patient.models.patient import PatientCreate, PatientUpdate, PatientPublic, PatientStatus
from modules.database.session import SessionDep
from modules.auth.controllers.log import log, LogType
from modules.impatient.models.admission import AdmissionPublic


router = APIRouter()

@router.get("/", response_model=list[PatientPublic])
def list_patients(
    session: SessionDep,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    status: PatientStatus | None = None,
    phone: str | None = None,
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
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_patient_all(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email,
        status=status,
        phone=phone,
        offset=offset,
        limit=limit,
        created_datetime=created_datetime,
        created_datetime__gt=created_datetime__gt,
        created_datetime__lt=created_datetime__lt,
        created_datetime__gte=created_datetime__gte,
        created_datetime__lte=created_datetime__lte,
        updated_datetime=updated_datetime,
        updated_datetime__gt=updated_datetime__gt,
        updated_datetime__lt=updated_datetime__lt,
        updated_datetime__gte=updated_datetime__gte,
        updated_datetime__lte=updated_datetime__lte,
    )


@router.get("/{id}/admissions/", response_model=list[AdmissionPublic])
def list_patients(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_patient_admissions(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )


@router.get("/{id}/", response_model=PatientPublic)
def retrieve_patient(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    patient = get_patient_by_id(session=session, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Staff not found")
    return patient





@router.post("/", response_model=PatientPublic)
def register_patient(
    patient_create: PatientCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = create_patient(patient=patient_create, session=session)
        log(staff_id=current_staff.id, path="post patient", model=patient, log_type=LogType.Post, session=session)
        return patient
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A patient with the provided details already exists"
        )


@router.put("/{id}/", response_model=PatientPublic)
def update(
    id: int,
    patient_update: PatientUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = update_patient(patient=patient_update, id=id, session=session)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        log(staff_id=current_staff.id, path="update patient", model=patient, log_type=LogType.Put, session=session)
        return patient
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error updating patient: {str(e)}")


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_patient(patient_id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    log(staff_id=current_staff.id, path="delete patient", model=None, log_type=LogType.Delete, session=session)
    return {"detail": "Patient deleted successfully"}