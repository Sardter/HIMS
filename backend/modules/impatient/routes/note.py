from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.impatient.controllers.note import get_note_all, get_note_by_id, create_note, update_note, delete_note
from modules.impatient.models.note import Note, NoteCreate, NoteUpdate, NotePublic
from modules.database.session import SessionDep

router = APIRouter()

@router.get("/", response_model=list[NotePublic])
def list_notes(
    session: SessionDep,
    text: str | None = None,
    admission_id: int | None = None,
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
    return get_note_all(
        session=session,
        text=text,
        admission_id=admission_id,
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


@router.get("/{id}/", response_model=NotePublic)
def retrieve_room(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    patient = get_note_by_id(session=session, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Staff not found")
    return patient


@router.post("/", response_model=NotePublic)
def register_room(
    patient_create: NoteCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = create_note(staff=patient_create, session=session)
        return patient
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A patient with the provided details already exists"
        )


@router.put("/{id}/", response_model=NotePublic)
def update(
    id: int,
    patient_update: NoteUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    staff = update_note(staff=patient_update, id=id, session=session)
    if not staff:
        raise HTTPException(status_code=404, detail="Patient not found")
    return staff


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_note(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}