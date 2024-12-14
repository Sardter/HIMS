from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse


from modules.auth.controllers.staff import get_staff_all, get_staff_by_id, register_staff, login_staff, update_staff, delete_staff, get_current_staff, get_staff_admissions, get_staff_logs, get_staff_notes
from modules.auth.models.staff import Staff, StaffCreate, StaffUpdate, StaffLogin, StaffPublic
from modules.database.session import SessionDep
from modules.impatient.models.admission import AdmissionPublic
from modules.impatient.models.note import NotePublic
from modules.auth.models.log import LogPublic

router = APIRouter()

@router.get("/", response_model=list[StaffPublic])
def list_staff(
    session: SessionDep,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    username: str | None = None,
    phone: str | None = None,
    offset: int = 0,
    limit: int = 10,
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
    current_staff: Staff = Depends(get_current_staff),
):
    return get_staff_all(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
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
def list_staff_admissions(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_staff_admissions(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )


@router.get("/{id}/notes/", response_model=list[NotePublic])
def list_staff_notes(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_staff_notes(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )


@router.get("/{id}/logs/", response_model=list[LogPublic])
def list_staff_logs(
    session: SessionDep,
    id: int,
    offset: int = 0,
    limit: int = 10,
    current_staff: Staff = Depends(get_current_staff),
):
    return get_staff_logs(
        id=id,
        session=session,
        offset=offset,
        limit=limit
    )


@router.get("/{id}/", response_model=StaffPublic)
def retrieve_staff(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    staff = get_staff_by_id(session=session, id=id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@router.get("/me/", response_model=StaffPublic)
def retrieve_me(
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    return current_staff

@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    staff = login_staff(staff=StaffLogin(username=form_data.username, passowrd=form_data.password), session=session)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    response = JSONResponse(content={"detail": "Login successful", "access_token": str(staff.id)})
    response.set_cookie(key="access_token", value=staff.id, httponly=True)
    return response


@router.post("/register", response_model=StaffPublic)
def register(
    staff_create: StaffCreate,
    session: SessionDep,
):
    try:
        staff = register_staff(staff=staff_create, session=session)
        return staff
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="A user with the provided details already exists"
        )


@router.put("/", response_model=StaffPublic)
def update(
    staff_update: StaffUpdate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    staff = update_staff(staff=staff_update, id=current_staff.id, session=session)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@router.delete("/", response_model=dict)
def delete(
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_staff(id=current_staff.id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"detail": "Staff deleted successfully"}