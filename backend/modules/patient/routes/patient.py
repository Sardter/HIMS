from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.patient.controllers.patient import get_patient_all, get_patient_by_id, create_patient, update_patient, delete_patient, get_patient_admissions
from modules.patient.models.patient import PatientCreate, PatientUpdate, PatientPublic, PatientStatus
from modules.database.session import SessionDep

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
        patient = create_patient(staff=patient_create, session=session)
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
    staff = update_patient(staff=patient_update, id=id, session=session)
    if not staff:
        raise HTTPException(status_code=404, detail="Patient not found")
    return staff


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_patient(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}