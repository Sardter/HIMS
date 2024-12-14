import streamlit as st
from utils import BackendClient

def register_view():
    st.title("Register New Staff")

    # If already logged in, show a message and possibly restrict registration
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.info("You are logged in. You can register another staff member if you have the appropriate permissions.")
    
    # The fields below depend on your backend staff model
    with st.form("register_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        phone = st.text_input("Phone")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Register")

    if submitted:
        if not (first_name and last_name and email and username and password):
            st.warning("Please fill in all required fields.")
            return

        client: BackendClient = st.session_state.get("client")
        if not client:
            st.error("No backend client found in session. Please go to the main page.")
            return

        staff_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": username,
            "phone": phone,
            "password": password
        }

        try:
            response = client.register_staff(staff_data=staff_data)
            st.success("Staff member registered successfully!")
        except Exception as e:
            st.error(f"Failed to register staff: {e}")

def main():
    if "client" not in st.session_state:
        st.error("Backend client not initialized. Please go to the main page.")
        return
    register_view()

if __name__ == "__main__":
    main()
