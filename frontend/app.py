import streamlit as st
from utils import BackendClient

st.set_page_config(page_title="Hospital Management System", layout="wide")

# Initialize the backend client
# Update the base_url to the actual endpoint of your backend
client = BackendClient(base_url="http://localhost:8000")

if "client" not in st.session_state:
    st.session_state["client"] = client

st.title("Hospital Management System")
st.write("Use the sidebar to navigate through different sections.")

# You can add a login flow here if necessary.
# For example:
# if "authenticated" not in st.session_state or not st.session_state.authenticated:
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         response = st.session_state["client"].login(username, password)
#         if "access_token" in response:
#             st.session_state.authenticated = True
# else:
#     st.sidebar.success("Logged in!")
