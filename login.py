import streamlit as st
from utils.auth import get_users, save_users, hash_password, verify_password
import re # Import the regular expressions library

st.set_page_config(page_title="Modern Login", page_icon="🔑", layout="centered", initial_sidebar_state="collapsed")

# --- Password Validation Function ---
def is_password_strong(password):
    """
    Checks if the password meets the strength requirements.
    Returns a list of messages for requirements that are not met.
    """
    errors = []
    if len(password) < 8:
        errors.append("be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        errors.append("contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("contain at least one lowercase letter")
    if not re.search(r"\d", password):
        errors.append("contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("contain at least one special character")
    
    return errors

def login_page():
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("assets/logo.png") # Corrected path for consistency
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")
        st.page_link("pages/profile.py", label="Go to your Profile Page")
        return

    choice = st.radio("", ["Login", "Sign Up"], horizontal=True)

    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                users = get_users()
                user = next((u for u in users if u["username"] == username), None)
                if user and verify_password(password, user["password"]):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    elif choice == "Sign Up":
        with st.form("signup_form"):
            new_username = st.text_input("Choose a Username")
            new_password = st.text_input("Choose a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Sign Up")

            if submitted:
                users = get_users()
                password_errors = is_password_strong(new_password)

                # --- VALIDATION LOGIC ---
                if not new_username or not new_password:
                    st.error("Username and password cannot be empty.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif any(u["username"] == new_username for u in users):
                    st.error("Username already exists.")
                elif password_errors:
                    # If there are password errors, display them
                    error_message = "Your password must:\n" + "\n".join([f"- {e}" for e in password_errors])
                    st.error(error_message)
                else:
                    # If all checks pass, create the new user
                    hashed_pass = hash_password(new_password)
                    users.append({
                        "username": new_username,
                        "password": hashed_pass,
                        "firstName": "",
                        "lastName": "",
                        "dob": None,
                        "avatar": "" # Add avatar field for new users
                    })
                    save_users(users)
                    st.success("You have successfully signed up! Please log in.")

if __name__ == "__main__":
    login_page()