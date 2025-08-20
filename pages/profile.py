import streamlit as st
from utils.auth import get_users, update_user_profile
from datetime import datetime, date

st.set_page_config(page_title="User Profile", page_icon="👤", layout="centered")

# --- HIDE THE SIDEBAR ---
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)


# Protect the page
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your profile.")
    st.page_link("login.py", label="Go to Login")
    st.stop()

st.title(f"Welcome to your profile, {st.session_state.username}!")
st.page_link("login.py", label="Back to Home Page")
st.markdown("---")

# --- USER DATA LOADING ---
users = get_users()
current_user = next((user for user in users if user['username'] == st.session_state.username), None)

# --- PROFILE FORM ---
with st.form("profile_form"):
    st.subheader("Edit Your Information")

    # Load existing data into form
    first_name = st.text_input("First Name", value=current_user.get("firstName", ""))
    last_name = st.text_input("Last Name", value=current_user.get("lastName", ""))

    # --- UPDATED DATE INPUT ---
    # Define the valid date range
    today = date.today()
    min_date = date(today.year - 100, today.month, today.day) # Allow ages up to 100

    dob_str = current_user.get("dob")
    if dob_str:
        # Convert the string from the JSON to a date object
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    else:
        # If no DoB is saved, default to a reasonable date like 18 years ago
        dob = date(today.year - 18, today.month, today.day)

    date_of_birth = st.date_input(
        "Date of Birth",
        value=dob,
        min_value=min_date,
        max_value=today
    )

    submitted = st.form_submit_button("Save Changes")
    if submitted:
        profile_data = {
            "firstName": first_name,
            "lastName": last_name,
            "dob": date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None
        }
        if update_user_profile(st.session_state.username, profile_data):
            st.success("Profile updated successfully!")
        else:
            st.error("Failed to update profile.")

st.markdown("---")

# --- LOGOUT BUTTON ---
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been successfully logged out.")
    st.switch_page("login.py")