from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.impatient.controllers.admission import get_admission_all, get_admission_by_id, create_admission, update_admission, delete_admission, get_admission_notes
from modules.impatient.models.admission import AdmissionCreate, AdmissionUpdate, AdmissionPublic
from modules.database.session import SessionDep
from modules.impatient.models.note import NotePublic
from modules.impatient.controllers.exceptions import RoomCapacityOverFlow, RoomDoesNotExist, PatientDoesNotExist, PatientAlreadyInRoom
from modules.auth.controllers.log import log, LogType


router = APIRouter()

@router.get("/", response_model=list[AdmissionPublic])
def list_admissions(
    session: SessionDep,
    patient_id: int | None = None,
    room_id: int | None = None,
    staff_id: int | None = None,
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
    return get_admission_all(
        session=session,
        patient_id=patient_id,
        room_id=room_id,
        staff_id=staff_id,
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


@router.get("/{id}/notes/", response_model=list[NotePublic])
def list_admission_notes(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_admission_notes(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )



@router.get("/{id}/", response_model=AdmissionPublic)
def retrieve_admission(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    admission = get_admission_by_id(session=session, id=id)
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return admission


@router.post("/", response_model=AdmissionPublic)
def post_admission(
    patient_create: AdmissionCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        admission = create_admission(admission=patient_create, session=session, staff_id=current_staff.id)
        log(staff_id=current_staff.id, model=admission, path="post admission", log_type=LogType.Post, session=session)
        return admission
    except RoomDoesNotExist:
        raise HTTPException(status_code=404, detail="Room Does not exist")
    except RoomCapacityOverFlow:
        raise HTTPException(status_code=400, detail="Not enough capacity in room")
    except PatientAlreadyInRoom:
        raise HTTPException(status_code=400, detail="Patient has been admitted to room already")
    except PatientDoesNotExist:
        raise HTTPException(status_code=404, detail="Patient Does not exist")


@router.put("/{id}/", response_model=AdmissionPublic)
def update(
    id: int,
    admission_update: AdmissionUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    admission = update_admission(admission=admission_update, id=id, session=session)
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    log(staff_id=current_staff.id, model=admission, path="update admission", log_type=LogType.Put, session=session)
    return admission


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_admission(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Admission not found")
    log(staff_id=current_staff.id, model=None, path="delete admission", log_type=LogType.Post, session=session)
    
    return {"detail": "Admission deleted successfully"}