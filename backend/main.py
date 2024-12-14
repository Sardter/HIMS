from typing import Union

from fastapi import FastAPI

from modules.database.engine import create_db_and_tables
from modules.auth.routes.staff import router as auth_router


create_db_and_tables()

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])