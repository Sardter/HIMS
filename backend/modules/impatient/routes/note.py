from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.impatient.controllers.note import get_note_all, get_note_by_id, create_note, update_note, delete_note
from modules.impatient.models.note import NoteCreate, NoteUpdate, NotePublic
from modules.database.session import SessionDep
from modules.auth.controllers.log import log, LogType


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
def retrieve_note(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    note = get_note_by_id(session=session, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=NotePublic)
def post_note(
    patient_create: NoteCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    note = create_note(note=patient_create, session=session, staff_id=current_staff.id)
    log(staff_id=current_staff.id, path="post note", model=note, log_type=LogType.Post, session=session)
    return note


@router.put("/{id}/", response_model=NotePublic)
def update(
    id: int,
    note_update: NoteUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    note = update_note(note=note_update, id=id, session=session)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    log(staff_id=current_staff.id, path="update note", model=note, log_type=LogType.Put, session=session)
    
    return note


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_note(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    log(staff_id=current_staff.id, path="delete note", model=None, log_type=LogType.Delete, session=session)
    
    return {"detail": "Note deleted successfully"}