import streamlit as st
from utils import BackendClient
from typing import Optional

def rooms_view():
    st.title("Rooms Management")

    # We will retrieve the backend client from session state
    client: BackendClient = st.session_state["client"]

    st.write("Use the filters below to search for rooms.")

    # Create filtering options
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        name_filter = st.text_input("Room Name (contains)")
    with col2:
        max_capacity_eq = st.number_input("Exact Capacity", min_value=0, value=0)
    with col3:
        max_capacity_gte = st.number_input("Capacity ≥", min_value=0, value=0)
    with col4:
        max_capacity_lte = st.number_input("Capacity ≤", min_value=0, value=0)

    # A small explanation:
    # The backend has filters like:
    # name, maximum_capacity, maximum_capacity__gte, maximum_capacity__lte, etc.
    # We'll conditionally add them based on user input.

    # Build the query parameters dictionary
    query_params = {}
    if name_filter:
        query_params["name"] = name_filter
    # If user provided exact capacity, it should override other capacity filters
    if max_capacity_eq > 0:
        query_params["maximum_capacity"] = max_capacity_eq
    else:
        # Only apply gte/lte if exact capacity is not set
        if max_capacity_gte > 0:
            query_params["maximum_capacity__gte"] = max_capacity_gte
        if max_capacity_lte > 0:
            query_params["maximum_capacity__lte"] = max_capacity_lte

    st.write("Adjust offset and limit for pagination if needed:")
    offset = st.number_input("Offset", min_value=0, value=0)
    limit = st.number_input("Limit", min_value=1, value=10)

    query_params["offset"] = offset
    query_params["limit"] = limit

    if st.button("Search"):
        # Fetch rooms from the backend
        with st.spinner("Fetching rooms..."):
            rooms_data = client.list_rooms(**query_params)
            st.success("Rooms fetched successfully!")
            
            # Display the rooms in a table
            if "results" in rooms_data:
                results = rooms_data["results"]
            else:
                # If no pagination structure, assume the entire list is returned
                results = rooms_data

            if results:
                st.table(results)
            else:
                st.info("No rooms found for the given filters.")

    st.write("---")
    st.write("### Create a new Room")

    # A simple form to create a new room
    with st.form("create_room_form"):
        new_room_name = st.text_input("Room Name", "")
        new_room_capacity = st.number_input("Maximum Capacity", min_value=1, value=1)
        submitted = st.form_submit_button("Create Room")
        if submitted and new_room_name:
            with st.spinner("Creating new room..."):
                room_data = {
                    "name": new_room_name,
                    "maximum_capacity": new_room_capacity
                }
                try:
                    response = client.create_room(room_data)
                    st.success(f"Room created successfully! ID: {response.get('id')}")
                except Exception as e:
                    st.error(f"Error creating room: {e}")

def main():
    # Ensure that the client is available in session
    if "client" not in st.session_state:
        st.error("No backend client found. Please go to the main page.")
        return

    rooms_view()

if __name__ == "__main__":
    main()
