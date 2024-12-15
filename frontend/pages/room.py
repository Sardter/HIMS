import streamlit as st
from utils import BackendClient

def rooms_view():
    st.title("Rooms Management")

    # We will retrieve the backend client from session state
    client: BackendClient = st.session_state["client"]

    st.write("Use the filters below to search for rooms.")
    
    # Create filtering options for searching rooms (if needed)
    name_filter = st.text_input("Room Name (contains)")
    max_capacity_eq = st.number_input("Exact Capacity", min_value=0, value=0)
    max_capacity_gte = st.number_input("Capacity ≥", min_value=0, value=0)
    max_capacity_lte = st.number_input("Capacity ≤", min_value=0, value=0)

    query_params = {}
    if name_filter:
        query_params["name"] = name_filter
    if max_capacity_eq > 0:
        query_params["maximum_capacity"] = max_capacity_eq
    else:
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
        with st.spinner("Fetching rooms..."):
            rooms_data = client.list_rooms(**query_params)
            st.success("Rooms fetched successfully!")

            results = rooms_data.get("results", []) if "results" in rooms_data else rooms_data
            if results:
                st.table(results)
            else:
                st.info("No rooms found for the given filters.")

    st.write("---")
    st.write("### Create a New Room")
    
    # Create room by entering details
    with st.form("create_room_form"):
        room_name = st.text_input("Room Name")
        room_capacity = st.number_input("Maximum Capacity", min_value=1)
        submitted_create = st.form_submit_button("Create Room")
        
        if submitted_create and room_name and room_capacity:
            with st.spinner("Creating room..."):
                room_data = {
                    "name": room_name,
                    "maximum_capacity": room_capacity
                }
                
                try:
                    response = client.create_room(room_data)  # Assuming this function is available in BackendClient
                    st.success(f"Room '{room_name}' created successfully!")
                except Exception as e:
                    st.error(f"Error creating room: {e}")

    st.write("---")
    st.write("### Update an Existing Room")
    
    # Update room by entering room ID and new values
    with st.form("update_room_form"):
        room_id = st.number_input("Room ID to update", min_value=1)
        new_room_name = st.text_input("New Room Name")
        new_room_capacity = st.number_input("New Maximum Capacity", min_value=1)
        submitted_update = st.form_submit_button("Update Room")
        
        if submitted_update and room_id and (new_room_name or new_room_capacity):
            with st.spinner("Updating room..."):
                room_data = {}
                if new_room_name:
                    room_data["name"] = new_room_name
                if new_room_capacity:
                    room_data["maximum_capacity"] = new_room_capacity
                
                try:
                    response = client.update_room(room_id, room_data)
                    st.success(f"Room ID {room_id} updated successfully!")
                except Exception as e:
                    st.error(f"Error updating room: {e}")

    st.write("---")
    st.write("### Delete a Room")
    
    # Delete room by entering room ID
    with st.form("delete_room_form"):
        room_id_to_delete = st.number_input("Room ID to delete", min_value=1)
        submitted_delete = st.form_submit_button("Delete Room")
        
        if submitted_delete and room_id_to_delete:
            with st.spinner("Deleting room..."):
                try:
                    response = client.delete_room(room_id_to_delete)
                    st.success(f"Room ID {room_id_to_delete} deleted successfully!")
                except Exception as e:
                    st.error(f"Error deleting room: {e}")

def main():
    if "client" not in st.session_state:
        st.error("No backend client found. Please go to the main page.")
        return

    rooms_view()

if __name__ == "__main__":
    main()
