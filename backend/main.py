from fastapi import FastAPI

from modules.database.engine import create_db_and_tables
from modules.auth.routes.staff import router as auth_router
from modules.patient.routes.patient import router as patient_router
from modules.impatient.routes.room import router as room_router
from modules.impatient.routes.admission import router as admission_router
from modules.impatient.routes.note import router as note_router
from modules.auth.routes.log import router as log_router


create_db_and_tables()

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(patient_router, prefix="/patient", tags=["Patients"])
app.include_router(room_router, prefix="/room", tags=["Rooms"])
app.include_router(admission_router, prefix="/admission", tags=["Admissions"])
app.include_router(note_router, prefix="/note", tags=["Notes"])
app.include_router(log_router, prefix="/log", tags=["Logs"])