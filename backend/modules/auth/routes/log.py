from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError


from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.auth.controllers.log import get_log_all, get_log_by_id, create_log, delete_log
from modules.auth.models.log import LogCreate, LogPublic
from modules.database.session import SessionDep

router = APIRouter()

@router.get("/", response_model=list[LogPublic])
def list_logs(
    session: SessionDep,
    text: str | None = None,
    staff_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_log_all(
        session=session,
        text=text,
        staff_id=staff_id,
        offset=offset,
        limit=limit,
    )


@router.get("/{id}/", response_model=LogPublic)
def retrieve_log(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    patient = get_log_by_id(session=session, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Staff not found")
    return patient


@router.post("/", response_model=LogPublic)
def create_log(
    patient_create: LogCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = create_log(staff=patient_create, session=session)
        return patient
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A patient with the provided details already exists"
        )


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_log(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}