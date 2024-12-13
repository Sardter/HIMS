from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    from modules.auth.models.log import Log
    from modules.auth.models.staff import Staff
    from modules.impatient.models.admission import Admission
    from modules.impatient.models.note import Note
    from modules.impatient.models.room import Room
    from modules.patient.models.patient import Patient
    
    SQLModel.metadata.create_all(engine)