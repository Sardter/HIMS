import streamlit as st
from utils import BackendClient
from datetime import datetime, time

def notes_view():
    st.title("Notes Management")

    if "client" not in st.session_state:
        st.error("No backend client found in session. Please go to the main page.")
        return

    client: BackendClient = st.session_state["client"]

    st.write("### Search and Filter Notes")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        text_filter = st.text_input("Text (contains)")
    with col2:
        admission_id_filter = st.number_input("Admission ID (optional)", min_value=0, value=0)
    with col3:
        staff_id_filter = st.number_input("Staff ID (optional)", min_value=0, value=0)
    with col4:
        offset = st.number_input("Offset", min_value=0, value=0)
        limit = st.number_input("Limit", min_value=1, value=10)

    query_params = {
        "offset": offset,
        "limit": limit
    }

    if text_filter.strip():
        query_params["text"] = text_filter.strip()
    if admission_id_filter > 0:
        query_params["admission_id"] = admission_id_filter
    if staff_id_filter > 0:
        query_params["staff_id"] = staff_id_filter

    search_button = st.button("Search Notes")

    if search_button:
        with st.spinner("Fetching notes..."):
            try:
                notes_data = client.list_notes(**query_params)
                st.success("Notes fetched successfully!")
                results = notes_data
                if results:
                    st.table(results)
                else:
                    st.info("No notes found with the given filters.")
            except Exception as e:
                st.error(f"Error fetching notes: {e}")

    st.write("---")

    st.write("### Create a New Note")
    with st.form("create_note_form"):
        new_text = st.text_area("Note Text", "")
        new_admission_id = st.number_input("Admission ID", min_value=1, value=1)
        new_staff_id = st.number_input("Staff ID", min_value=1, value=1)

        submitted = st.form_submit_button("Create Note")

        if submitted:
            if not new_text.strip():
                st.warning("Please provide note text.")
            else:
                note_data = {
                    "text": new_text.strip(),
                    "admission_id": new_admission_id,
                    "staff_id": new_staff_id
                }
                with st.spinner("Creating new note..."):
                    try:
                        response = client.create_note(note_data=note_data)
                        st.success(f"Note created successfully! ID: {response.get('id')}")
                    except Exception as e:
                        st.error(f"Error creating note: {e}")

    st.write("---")

    st.write("### Delete a Note")
    delete_note_id = st.number_input("Enter Note ID to Delete", min_value=1)
    delete_button = st.button("Delete Note")

    if delete_button:
        with st.spinner("Deleting note..."):
            try:
                response = client.delete_note(note_id=delete_note_id)
                if response:
                    st.success(f"Note with ID {delete_note_id} deleted successfully!")
                else:
                    st.error(f"Note with ID {delete_note_id} not found.")
            except Exception as e:
                st.error(f"Error deleting note: {e}")

    st.write("---")

    st.write("### Update a Note")
    update_note_id = st.number_input("Enter Note ID to Update", min_value=1)
    
    with st.form("update_note_form"):
        updated_text = st.text_area("Updated Note Text", "")
        updated_admission_id = st.number_input("Updated Admission ID", min_value=1)
        updated_staff_id = st.number_input("Updated Staff ID", min_value=1)

        update_submit_button = st.form_submit_button("Update Note")

        if update_submit_button:
            if not updated_text.strip():
                st.warning("Please provide updated note text.")
            else:
                note_data = {
                    "text": updated_text.strip(),
                    "admission_id": updated_admission_id,
                    "staff_id": updated_staff_id
                }
                with st.spinner("Updating note..."):
                    try:
                        response = client.update_note(note_id=update_note_id, note_data=note_data)
                        if response:
                            st.success(f"Note with ID {update_note_id} updated successfully!")
                        else:
                            st.error(f"Note with ID {update_note_id} not found.")
                    except Exception as e:
                        st.error(f"Error updating note: {e}")

def main():
    notes_view()

if __name__ == "__main__":
    main()
