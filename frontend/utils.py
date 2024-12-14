import requests
from datetime import datetime
from typing import Optional
from enum import Enum

class PatientStatus(str, Enum):
    Registered = "R"
    Admitted = "A"
    Discharged = "D"


class BackendClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.token = None

    def set_token(self, token: str):
        """Set the authentication token for subsequent requests."""
        self.token = token

    def _headers(self):
        """Construct headers including authorization token if available."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _get(self, endpoint: str, params: dict = None):
        """Send a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict = None):
        """Send a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, data: dict = None):
        """Send a PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.put(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint: str, params: dict = None):
        """Send a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.delete(url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()

    # ------------------------------
    # Authentication/Staff Endpoints
    # ------------------------------
    def login(self, username: str, password: str):
        """
        Login and retrieve an access token.
        """
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        json_resp = response.json()

        token = json_resp.get("access_token")
        if token:
            self.set_token(token)
        return json_resp

    def logout(self):
        """Logout by clearing the token locally."""
        self.set_token(None)

    def register_staff(self, staff_data: dict):
        """Register a new staff member."""
        return self._post("/auth/register", data=staff_data)

    def get_current_staff(self):
        """Retrieve the currently logged-in staff's details."""
        return self._get("/auth/me/")

    def update_current_staff(self, staff_data: dict):
        """Update the current staff member's profile."""
        return self._put("/auth/", data=staff_data)

    def delete_current_staff(self):
        """Delete the current staff member."""
        return self._delete("/auth/")

    def get_staff(self, staff_id: int):
        """Retrieve a staff member by ID."""
        return self._get(f"/auth/{staff_id}/")

    def list_staff(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
    ):
        """List staff with extensive filtering options."""
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username,
            "phone": phone,
            "offset": offset,
            "limit": limit,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/auth/", params=params)

    def list_staff_admissions(self, staff_id: int, offset: int = 0, limit: int = 10):
        """List admissions associated with a staff member."""
        return self._get(f"/auth/{staff_id}/admissions/", params={"offset": offset, "limit": limit})

    def list_staff_notes(self, staff_id: int, offset: int = 0, limit: int = 10):
        """List notes created by a staff member."""
        return self._get(f"/auth/{staff_id}/notes/", params={"offset": offset, "limit": limit})

    def list_staff_logs(self, staff_id: int, offset: int = 0, limit: int = 10):
        """List logs associated with a staff member."""
        return self._get(f"/auth/{staff_id}/logs/", params={"offset": offset, "limit": limit})

    # ------------------------------
    # Patient Endpoints
    # ------------------------------
    def create_patient(self, patient_data: dict):
        """Create a new patient record."""
        return self._post("/patient", data=patient_data)

    def get_patient(self, patient_id: int):
        """Retrieve a patient by ID."""
        return self._get(f"/patient/{patient_id}/")

    def update_patient(self, patient_id: int, patient_data: dict):
        """Update patient details."""
        return self._put(f"/patient/{patient_id}/", data=patient_data)

    def delete_patient(self, patient_id: int):
        """Delete a patient record."""
        return self._delete(f"/patient/{patient_id}/")

    def list_patients(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[PatientStatus] = None,
        phone: Optional[str] = None,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """List patients with extensive filtering options."""
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "status": status.value if status else None,
            "phone": phone,
            "offset": offset,
            "limit": limit,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/patient/", params=params)

    def list_patient_admissions(self, patient_id: int, offset: int = 0, limit: int = 10):
        """List admissions for a given patient."""
        return self._get(f"/patient/{patient_id}/admissions/", params={"offset": offset, "limit": limit})

    # ------------------------------
    # Room Endpoints
    # ------------------------------
    def create_room(self, room_data: dict):
        """Create a new room."""
        return self._post("/room/", data=room_data)

    def get_room(self, room_id: int):
        """Retrieve a room by ID."""
        return self._get(f"/room/{room_id}/")

    def update_room(self, room_id: int, room_data: dict):
        """Update room details."""
        return self._put(f"/room/{room_id}/", data=room_data)

    def delete_room(self, room_id: int):
        """Delete a room."""
        return self._delete(f"/room/{room_id}/")

    def list_rooms(
        self,
        name: Optional[str] = None,
        maximum_capacity: Optional[int] = None,
        maximum_capacity__gt: Optional[int] = None,
        maximum_capacity__lt: Optional[int] = None,
        maximum_capacity__gte: Optional[int] = None,
        maximum_capacity__lte: Optional[int] = None,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """List rooms with extensive filtering options."""
        params = {
            "name": name,
            "maximum_capacity": maximum_capacity,
            "maximum_capacity__gt": maximum_capacity__gt,
            "maximum_capacity__lt": maximum_capacity__lt,
            "maximum_capacity__gte": maximum_capacity__gte,
            "maximum_capacity__lte": maximum_capacity__lte,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
            "offset": offset,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/room/", params=params)

    def list_room_admissions(self, room_id: int, offset: int = 0, limit: int = 10):
        """List admissions for a given room."""
        return self._get(f"/room/{room_id}/admissions/", params={"offset": offset, "limit": limit})

    # ------------------------------
    # Admission Endpoints
    # ------------------------------
    def create_admission(self, admission_data: dict):
        """Create a new admission."""
        return self._post("/admission", data=admission_data)

    def get_admission(self, admission_id: int):
        """Retrieve an admission record."""
        return self._get(f"/admission/{admission_id}/")

    def update_admission(self, admission_id: int, admission_data: dict):
        """Update an admission record."""
        return self._put(f"/admission/{admission_id}/", data=admission_data)

    def delete_admission(self, admission_id: int):
        """Delete an admission."""
        return self._delete(f"/admission/{admission_id}/")

    def list_admissions(
        self,
        patient_id: Optional[int] = None,
        room_id: Optional[int] = None,
        staff_id: Optional[int] = None,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """List admissions with extensive filtering options."""
        params = {
            "patient_id": patient_id,
            "room_id": room_id,
            "staff_id": staff_id,
            "offset": offset,
            "limit": limit,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
        }

        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/admission/", params=params)

    def list_admission_notes(self, admission_id: int, offset: int = 0, limit: int = 10):
        """List notes related to a specific admission."""
        return self._get(f"/admission/{admission_id}/notes/", params={"offset": offset, "limit": limit})

    # ------------------------------
    # Note Endpoints
    # ------------------------------
    def create_note(self, note_data: dict):
        """Create a new note."""
        return self._post("/note/", data=note_data)

    def get_note(self, note_id: int):
        """Retrieve a note."""
        return self._get(f"/note/{note_id}/")

    def update_note(self, note_id: int, note_data: dict):
        """Update a note."""
        return self._put(f"/note/{note_id}/", data=note_data)

    def delete_note(self, note_id: int):
        """Delete a note."""
        return self._delete(f"/note/{note_id}/")

    def list_notes(
        self,
        text: Optional[str] = None,
        admission_id: Optional[int] = None,
        staff_id: Optional[int] = None,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """List notes with extensive filtering options."""
        params = {
            "text": text,
            "admission_id": admission_id,
            "staff_id": staff_id,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
            "offset": offset,
            "limit": limit,
        }

        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/note/", params=params)

    # ------------------------------
    # Log Endpoints
    # ------------------------------
    def list_logs(
        self,
        text: Optional[str] = None,
        staff_id: Optional[int] = None,
        created_datetime: Optional[datetime] = None,
        created_datetime__gt: Optional[datetime] = None,
        created_datetime__lt: Optional[datetime] = None,
        created_datetime__gte: Optional[datetime] = None,
        created_datetime__lte: Optional[datetime] = None,
        updated_datetime: Optional[datetime] = None,
        updated_datetime__gt: Optional[datetime] = None,
        updated_datetime__lt: Optional[datetime] = None,
        updated_datetime__gte: Optional[datetime] = None,
        updated_datetime__lte: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """List logs with extensive filtering options."""
        params = {
            "text": text,
            "staff_id": staff_id,
            "created_datetime": created_datetime.isoformat() if created_datetime else None,
            "created_datetime__gt": created_datetime__gt.isoformat() if created_datetime__gt else None,
            "created_datetime__lt": created_datetime__lt.isoformat() if created_datetime__lt else None,
            "created_datetime__gte": created_datetime__gte.isoformat() if created_datetime__gte else None,
            "created_datetime__lte": created_datetime__lte.isoformat() if created_datetime__lte else None,
            "updated_datetime": updated_datetime.isoformat() if updated_datetime else None,
            "updated_datetime__gt": updated_datetime__gt.isoformat() if updated_datetime__gt else None,
            "updated_datetime__lt": updated_datetime__lt.isoformat() if updated_datetime__lt else None,
            "updated_datetime__gte": updated_datetime__gte.isoformat() if updated_datetime__gte else None,
            "updated_datetime__lte": updated_datetime__lte.isoformat() if updated_datetime__lte else None,
            "offset": offset,
            "limit": limit,
        }

        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/log/", params=params)

    def retrieve_log(self, log_id: int):
        """Retrieve a single log by ID."""
        return self._get(f"/log/{log_id}/")

    def create_log(self, log_data: dict):
        """Create a new log entry."""
        return self._post("/log/", data=log_data)

    def delete_log(self, log_id: int):
        """Delete a log entry by ID."""
        return self._delete(f"/log/{log_id}/")


# Example usage:
# client = BackendClient(base_url="http://localhost:8000")
# login_response = client.login(username="test_user", password="secret")
# rooms = client.list_rooms(name="ICU", maximum_capacity__gte=5)
# print(rooms)
