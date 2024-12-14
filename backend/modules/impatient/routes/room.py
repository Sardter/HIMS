from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from modules.auth.controllers.staff import get_current_staff
from modules.auth.models.staff import Staff
from modules.impatient.controllers.room import get_room_all, get_room_by_id, create_room, update_room, delete_room, get_room_admissions
from modules.impatient.models.room import Room, RoomCreate, RoomUpdate, RoomPublic
from modules.database.session import SessionDep
from modules.impatient.models.admission import AdmissionPublic

router = APIRouter()

@router.get("/", response_model=list[RoomPublic])
def list_rooms(
    session: SessionDep,
    name: str | None = None,
    maximum_capacity: int | None = None,
    maximum_capacity__gt: int | None = None,
    maximum_capacity__lt: int | None = None,
    maximum_capacity__gte: int | None = None,
    maximum_capacity__lte: int | None = None,
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
    return get_room_all(
        session=session,
        name=name,
        maximum_capacity=maximum_capacity,
        maximum_capacity__gt=maximum_capacity__gt,
        maximum_capacity__lt=maximum_capacity__lt,
        maximum_capacity__gte=maximum_capacity__gte,
        maximum_capacity__lte=maximum_capacity__lte,
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
def list_room_admissions(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_room_admissions(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )



@router.get("/{id}/", response_model=RoomPublic)
def retrieve_room(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    patient = get_room_by_id(session=session, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Staff not found")
    return patient


@router.post("/", response_model=RoomPublic)
def register_room(
    patient_create: RoomCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    try:
        patient = create_room(staff=patient_create, session=session)
        return patient
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A patient with the provided details already exists"
        )


@router.put("/{id}/", response_model=RoomPublic)
def update(
    id: int,
    patient_update: RoomUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    staff = update_room(staff=patient_update, id=id, session=session)
    if not staff:
        raise HTTPException(status_code=404, detail="Patient not found")
    return staff


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_room(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted successfully"}