import streamlit as st

# Set page configuration
st.set_page_config(page_title="User Profile", page_icon="👤", layout="centered")

# Protect the page - redirect to login if not logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your profile.")
    st.page_link("login.py", label="Go to Login")
    st.stop()

# Page content for logged-in users
st.title(f"Welcome to your profile, {st.session_state.username}!")
st.markdown("---")
st.write("This is your personal profile page. You can add more information here.")

# Example of displaying user-specific data
st.subheader("Your Details")
st.write(f"**Username:** {st.session_state.username}")