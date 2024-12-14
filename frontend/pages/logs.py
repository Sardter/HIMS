import streamlit as st
from utils import BackendClient
from datetime import datetime, time

def logs_view():
    st.title("Logs Management")

    # Ensure client is in session
    if "client" not in st.session_state:
        st.error("No backend client found in session. Please go back to the main page.")
        return

    client: BackendClient = st.session_state["client"]

    st.write("### Search and Filter Logs")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        text_filter = st.text_input("Text (contains)")
    with col2:
        staff_id_filter = st.number_input("Staff ID (optional)", min_value=0, value=0)
    with col3:
        offset = st.number_input("Offset", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=1, value=10)

    # Optional exact created date filter
    #created_date = st.date_input("Created Date (optional)")
    #created_datetime = None
    #if created_date:
    #    created_datetime = datetime.combine(created_date, time(0, 0))

    # Build query parameters
    query_params = {
        "offset": offset,
        "limit": limit
    }

    if text_filter.strip():
        query_params["text"] = text_filter.strip()
    if staff_id_filter > 0:
        query_params["staff_id"] = staff_id_filter
    #if created_datetime:
    #    query_params["created_datetime"] = created_datetime

    search_button = st.button("Search Logs")

    if search_button:
        with st.spinner("Fetching logs..."):
            try:
                logs_data = client.list_logs(**query_params)
                st.success("Logs fetched successfully!")
                results = logs_data
                if results:
                    st.table(results)
                else:
                    st.info("No logs found with the given filters.")
            except Exception as e:
                st.error(f"Error fetching logs: {e}")

    st.write("---")
    st.write("### Create a New Log Entry")

    # A form to create a new log entry
    with st.form("create_log_form"):
        new_text = st.text_area("Log Text", "")
        new_staff_id = st.number_input("Staff ID", min_value=1, value=1)

        submitted = st.form_submit_button("Create Log")

        if submitted:
            # Basic validation
            if not new_text.strip():
                st.warning("Please provide log text.")
            else:
                log_data = {
                    "text": new_text.strip(),
                    "staff_id": new_staff_id
                }
                with st.spinner("Creating new log entry..."):
                    try:
                        response = client.create_log(log_data=log_data)
                        st.success(f"Log created successfully! ID: {response.get('id')}")
                    except Exception as e:
                        st.error(f"Error creating log entry: {e}")

def main():
    logs_view()

if __name__ == "__main__":
    main()