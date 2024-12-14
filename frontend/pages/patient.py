import streamlit as st
from utils import BackendClient, PatientStatus

def patients_view():
    st.title("Patients Management")

    # Ensure client is in session
    if "client" not in st.session_state:
        st.error("No backend client found in session. Please go to the main page.")
        return

    client: BackendClient = st.session_state["client"]

    # Search and Filter Section
    st.write("### Search and Filter Patients")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        first_name_filter = st.text_input("First Name")
        last_name_filter = st.text_input("Last Name")

    with col2:
        email_filter = st.text_input("Email")
        phone_filter = st.text_input("Phone")

    with col3:
        status_filter = st.selectbox("Status", options=["", "Registered", "Admitted", "Discharged"], index=0)
        gender_filter = st.selectbox("Gender", options=["", "Male", "Female", "Other"], index=0)

    offset = st.number_input("Offset", min_value=0, value=0)
    limit = st.number_input("Limit", min_value=1, value=10)

    # Build query parameters
    query_params = {
        "first_name": first_name_filter.strip() if first_name_filter.strip() else None,
        "last_name": last_name_filter.strip() if last_name_filter.strip() else None,
        "email": email_filter.strip() if email_filter.strip() else None,
        "phone": phone_filter.strip() if phone_filter.strip() else None,
        "offset": offset,
        "limit": limit
    }

    if status_filter:
        # Map the user-friendly status to the enum value
        status_map = {
            "Registered": PatientStatus.Registered,
            "Admitted": PatientStatus.Admitted,
            "Discharged": PatientStatus.Discharged
        }
        query_params["status"] = status_map.get(status_filter)

    if gender_filter:
        # Assume the backend accepts gender as a string: "Male", "Female", or "Other"
        query_params["gender"] = gender_filter

    search_button = st.button("Search")

    if search_button:
        with st.spinner("Fetching patients..."):
            try:
                patients_data = client.list_patients(**query_params)
                st.success("Patients fetched successfully!")
                # Check if response contains a 'results' key (pagination structure)
                results = patients_data
                if results:
                    st.table(results)
                else:
                    st.info("No patients found with the given filters.")
            except Exception as e:
                st.error(f"Error fetching patients: {e}")

    st.write("---")
    st.write("### Create a New Patient")

    # A form to create a new patient
    with st.form("create_patient_form"):
        new_first_name = st.text_input("First Name", "")
        new_last_name = st.text_input("Last Name", "")
        new_email = st.text_input("Email", "")
        new_phone = st.text_input("Phone", "")
        
        # Patient status selection
        new_status_str = st.selectbox("Status", options=["Registered", "Admitted", "Discharged"])
        status_map = {
            "Registered": PatientStatus.Registered,
            "Admitted": PatientStatus.Admitted,
            "Discharged": PatientStatus.Discharged
        }
        new_status = status_map[new_status_str]

        # Gender selection
        new_gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=0)

        submitted = st.form_submit_button("Create Patient")

        if submitted:
            # Basic validation
            if not new_first_name.strip() or not new_last_name.strip():
                st.warning("First name and last name are required.")
            else:
                patient_data = {
                    "first_name": new_first_name.strip(),
                    "last_name": new_last_name.strip(),
                    "email": new_email.strip(),
                    "phone": new_phone.strip(),
                    "status": new_status.value,
                    "gender": new_gender
                }
                with st.spinner("Creating new patient..."):
                    try:
                        response = client.create_patient(patient_data=patient_data)
                        st.success(f"Patient created successfully! ID: {response.get('id')}")
                    except Exception as e:
                        st.error(f"Error creating patient: {e}")

def main():
    patients_view()

if __name__ == "__main__":
    main()
