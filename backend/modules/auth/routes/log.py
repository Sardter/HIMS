from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

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
    return get_log_all(
        session=session,
        text=text,
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


@router.get("/{id}/", response_model=LogPublic)
def retrieve_log(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    log = get_log_by_id(session=session, id=id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.post("/", response_model=LogPublic)
def post_log(
    log_create: LogCreate,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    log = create_log(log=log_create, session=session, staff_id=current_staff.id)
    return log


@router.delete("/{id}/", response_model=dict)
def delete(
    id: int,
    session: SessionDep,
    current_staff: Staff = Depends(get_current_staff),
):
    success = delete_log(id=id, session=session)
    if not success:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"detail": "Log deleted successfully"}