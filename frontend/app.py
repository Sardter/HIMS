import streamlit as st
from utils import BackendClient

st.set_page_config(page_title="Hospital Management System", layout="wide")

client = BackendClient(base_url="http://localhost:8000")

if "client" not in st.session_state:
    st.session_state["client"] = client

st.title("Hospital Management System")
st.write("Use the sidebar to navigate through different sections.")