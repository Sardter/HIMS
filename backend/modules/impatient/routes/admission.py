from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.impatient.controllers.admission import get_admission_all, get_admission_by_id, create_admission, update_admission, delete_admission
from modules.impatient.models.admission import Admission, AdmissionCreate, AdmissionUpdate, AdmissionPublic
from modules.database.session import SessionDep

router = APIRouter()

@router.get("/", response_model=list[AdmissionPublic])
def list_admissions(
    session: SessionDep,
    patient_id: int | None = None,
    room_id: int | None = None,
    staff_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_admission_all(
        session=session,
        patient_id=patient_id,
        room_id=room_id,
        staff_id=staff_id,
        offset=offset,
        limit=limit,
    )


@router.get("/{id}/", response_model=AdmissionPublic)
def retrieve_admission(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    patient = get_admission_by_id(session=session, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Staff not found")
    return patient


@router.post("/", response_model=AdmissionPublic)
def create_admission(
    patient_create: AdmissionCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = create_admission(staff=patient_create, session=session)
        return patient
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A patient with the provided details already exists"
        )


@router.put("/{id}/", response_model=AdmissionPublic)
def update(
    id: int,
    patient_update: AdmissionPublic,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    staff = update_admission(staff=patient_update, id=id, session=session)
    if not staff:
        raise HTTPException(status_code=404, detail="Patient not found")
    return staff


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_admission(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}