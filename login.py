import streamlit as st
from utils.auth import get_users, save_users, hash_password, verify_password

st.set_page_config(page_title="Modern Login", page_icon="🔑", layout="centered")

# --- HIDE THE SIDEBAR ---
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)


def login_page():
    st.title("Modern Login & Sign Up")
    st.markdown("---")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")
        st.page_link("pages/profile.py", label="Go to your Profile")
        return

    choice = st.radio("Login or Sign Up", ["Login", "Sign Up"], horizontal=True)

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
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif any(u["username"] == new_username for u in users):
                    st.error("Username already exists.")
                elif not new_username or not new_password:
                    st.error("Username and password cannot be empty.")
                else:
                    hashed_pass = hash_password(new_password)
                    users.append({
                        "username": new_username,
                        "password": hashed_pass,
                        "firstName": "",
                        "lastName": "",
                        "dob": None
                    })
                    save_users(users)
                    st.success("You have successfully signed up! Please log in.")

if __name__ == "__main__":
    login_page()