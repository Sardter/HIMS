import streamlit as st
from utils import BackendClient

def login_view():
    st.title("Login")

    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.success("You are already logged in.")
        return

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username and password:
            client: BackendClient = st.session_state.get("client")
            if not client:
                st.error("No backend client found in session. Please go back to the main page.")
                return

            try:
                response = client.login(username, password)
                if "access_token" in response:
                    st.session_state["authenticated"] = True
                    st.success("Login successful!")
                    st.success("Login successful! Please return to the main page or refresh.")
                else:
                    st.error("Failed to retrieve token. Please check your credentials and try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide a username and password.")

def main():
    if "client" not in st.session_state:
        st.error("Backend client not initialized. Please go to the main page.")
        return
    login_view()

if __name__ == "__main__":
    main()
