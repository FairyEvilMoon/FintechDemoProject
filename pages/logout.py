import streamlit as st

# Set page configuration
st.set_page_config(page_title="Logout", page_icon="🔒", layout="centered")

st.title("Logout")
st.markdown("---")

if st.button("Confirm Logout"):
    # Reset session state variables
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been successfully logged out.")
    st.page_link("login.py", label="Go to Login Page")