import streamlit as st
from utils import BackendClient

def admissions_view():
    st.title("Admissions Management")

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
        offset = st.number_input("Offset", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=1, value=10)

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

    search_button = st.button("Search Admissions")

    if search_button:
        with st.spinner("Fetching admissions..."):
            try:
                admissions_data = client.list_admissions(**query_params)
                st.success("Admissions fetched successfully!")
                results = admissions_data
                if results:
                    st.table(results)
                else:
                    st.info("No admissions found with the given filters.")
            except Exception as e:
                st.error(f"Error fetching admissions: {e}")

    st.write("---")
    st.write("### Create a New Admission")

    with st.form("create_admission_form"):
        new_patient_id = st.number_input("Patient ID", min_value=1, value=1)
        new_room_id = st.number_input("Room ID", min_value=1, value=1)
        new_staff_id = st.number_input("Staff ID", min_value=1, value=1)
        submitted_create = st.form_submit_button("Create Admission")

        if submitted_create:
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
                        print(admission_data)
                        response = client.create_admission(admission_data=admission_data)
                        st.success(f"Admission created successfully! ID: {response.get('id')}")
                    except Exception as e:
                        if "Room Does not exist" in str(e):
                            st.error("Room does not exist.")
                        elif "Not enough capacity in room" in str(e):
                            st.error("Not enough capacity in the room.")
                        elif "Patient has been admitted to room already" in str(e):
                            st.error("Patient is already in the room.")
                        elif "Patient Does not exist" in str(e):
                            st.error("Patient does not exist.")
                        else:
                            st.error(f"Error creating admission: {e}")

    st.write("---")
    st.write("### Update an Admission")

    with st.form("update_admission_form"):
        admission_id = st.number_input("Admission ID", min_value=1, value=1)
        update_patient_id = st.number_input("Patient ID", min_value=1, value=1)
        update_room_id = st.number_input("Room ID", min_value=1, value=1)
        update_staff_id = st.number_input("Staff ID", min_value=1, value=1)
        submitted_update = st.form_submit_button("Update Admission")

        if submitted_update:
            if update_patient_id <= 0 or update_room_id <= 0 or update_staff_id <= 0:
                st.warning("Please provide valid Patient ID, Room ID, and Staff ID.")
            else:
                admission_update_data = {
                    "patient_id": int(update_patient_id),
                    "room_id": int(update_room_id),
                    "staff_id": int(update_staff_id),
                }

                with st.spinner("Updating admission..."):
                    try:
                        response = client.update_admission(admission_id, admission_update_data)
                        st.success(f"Admission updated successfully! ID: {response.get('id')}")
                    except Exception as e:
                        st.error(f"Error updating admission: {e}")

    st.write("---")
    st.write("### Delete an Admission")

    with st.form("delete_admission_form"):
        delete_admission_id = st.number_input("Admission ID to delete", min_value=1, value=1)
        submitted_delete = st.form_submit_button("Delete Admission")

        if submitted_delete:
            with st.spinner("Deleting admission..."):
                try:
                    response = client.delete_admission(delete_admission_id)
                    st.success(f"Admission deleted successfully! ID: {delete_admission_id}")
                except Exception as e:
                    st.error(f"Error deleting admission: {e}")

def main():
    admissions_view()

if __name__ == "__main__":
    main()
