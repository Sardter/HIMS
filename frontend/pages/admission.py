import streamlit as st
from utils import BackendClient
from datetime import datetime, time

def admissions_view():
    st.title("Admissions Management")

    # Ensure client is in session
    if "client" not in st.session_state:
        st.error("No backend client found in session. Please go to the main page.")
        return

    client: BackendClient = st.session_state["client"]

    st.write("### Search and Filter Admissions")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        patient_id_filter = st.number_input("Patient ID (optional)", min_value=0, value=0)
    with col2:
        room_id_filter = st.number_input("Room ID (optional)", min_value=0, value=0)
    with col3:
        staff_id_filter = st.number_input("Staff ID (optional)", min_value=0, value=0)
    with col4:
        # Pagination
        offset = st.number_input("Offset", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=1, value=10)

    # Optional date filters (exact created_datetime)
    # In reality you might want to use created_datetime__gt/lt/gte/lte
    # For simplicity, we just show one exact filter here.
    #created_date = st.date_input("Created Date (optional)")
    #created_datetime = None
    #if created_date:
        # Convert date to a datetime object at midnight
    #    created_datetime = datetime.combine(created_date, time(0, 0))

    # Build query parameters
    query_params = {
        "offset": offset,
        "limit": limit,
    }
    if patient_id_filter > 0:
        query_params["patient_id"] = patient_id_filter
    if room_id_filter > 0:
        query_params["room_id"] = room_id_filter
    if staff_id_filter > 0:
        query_params["staff_id"] = staff_id_filter
    #if created_datetime:
    #    query_params["created_datetime"] = created_datetime

    search_button = st.button("Search Admissions")

    if search_button:
        with st.spinner("Fetching admissions..."):
            try:
                admissions_data = client.list_admissions(**query_params)
                st.success("Admissions fetched successfully!")
                # Check if response contains 'results' (for pagination)
                results = admissions_data
                if results:
                    st.table(results)
                else:
                    st.info("No admissions found with the given filters.")
            except Exception as e:
                st.error(f"Error fetching admissions: {e}")

    st.write("---")
    st.write("### Create a New Admission")

    # A form to create a new admission
    with st.form("create_admission_form"):
        new_patient_id = st.number_input("Patient ID", min_value=1, value=1)
        new_room_id = st.number_input("Room ID", min_value=1, value=1)
        new_staff_id = st.number_input("Staff ID", min_value=1, value=1)
        submitted = st.form_submit_button("Create Admission")

        if submitted:
            # Basic validation: ensure IDs are provided
            if new_patient_id <= 0 or new_room_id <= 0 or new_staff_id <= 0:
                st.warning("Please provide valid Patient ID, Room ID, and Staff ID.")
            else:
                admission_data = {
                    "patient_id": new_patient_id,
                    "room_id": new_room_id,
                    "staff_id": new_staff_id,
                }
                with st.spinner("Creating new admission..."):
                    try:
                        response = client.create_admission(admission_data=admission_data)
                        st.success(f"Admission created successfully! ID: {response.get('id')}")
                    except Exception as e:
                        st.error(f"Error creating admission: {e}")

def main():
    admissions_view()

if __name__ == "__main__":
    main()
