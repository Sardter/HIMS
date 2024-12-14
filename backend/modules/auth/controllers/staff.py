from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import select

from modules.auth.models.staff import Staff, StaffCreate, StaffUpdate, StaffLogin
from modules.database.session import SessionDep

from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_staff_all(
        *,
        session: SessionDep,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        username: str | None = None,
        phone: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Staff]:
    query = select(Staff).offset(offset).limit(limit)
    filters = [
        Staff.first_name.ilike(f"%{first_name}%") if first_name is not None else None,
        Staff.last_name.ilike(f"%{last_name}%") if last_name is not None else None,
        Staff.email.ilike(f"%{email}%") if email is not None else None,
        Staff.username.ilike(f"%{username}%") if username is not None else None,
        Staff.phone.ilike(f"%{phone}%") if phone is not None else None,
    ]
    
    filters = [filter for filter in filters if filter is not None]
    
    if filters:
        query = query.where(*filters)
    
    return session.exec(query).all()


def get_staff_by_id( *, session: SessionDep, id: int) -> Staff | None:
    return session.get(Staff, id)


def __hash_password( password: str) -> str:
    return pbkdf2_sha256.hash(password)


def __verify_password( password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)


def login_staff( *, staff: StaffLogin, session: SessionDep) -> Staff | None:
    db_staff = session.exec(select(Staff).where(Staff.username == staff.username)).first()
    if db_staff is None or not __verify_password(staff.passowrd, db_staff.hashed_password):
        return None
    return db_staff


def register_staff( *, staff: StaffCreate, session: SessionDep) -> Staff | None:
    hashed_passowrd = __hash_password(staff.password)
    db_staff = Staff.model_validate(staff, update={"hashed_password": hashed_passowrd})
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def update_staff(*, id: int, staff: StaffUpdate, session: SessionDep) -> Staff | None:
    db_staff = session.get(Staff, id)
    if not db_staff:
        return None
    staff_data = staff.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in staff_data:
        password = staff_data["password"]
        hashed_password = __hash_password(password)
        extra_data["hashed_password"] = hashed_password
    db_staff.sqlmodel_update(staff_data, update=extra_data)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


def delete_staff(*, id: int, session: SessionDep) -> bool:
    db_staff = session.get(Staff, id)
    if db_staff is None:
        return False
    session.delete(db_staff)
    session.commit()
    return True


def get_current_staff(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> Staff:
    staff = session.exec(select(Staff).where(Staff.id == int(token))).first()
    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return staff