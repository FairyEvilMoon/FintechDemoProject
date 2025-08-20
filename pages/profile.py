import streamlit as st
from utils.auth import get_users, update_user_profile
from datetime import datetime, date

st.set_page_config(page_title="User Profile", page_icon="👤", layout="centered")

# ---------- Minimal styling ----------
st.markdown("""
<style>
/* Center max-width */
.main > div { max-width: 820px; margin: auto; }

/* Card look */
.card { border: 1px solid #e6e6e6; border-radius: 12px; padding: 20px; background: #fff; }
.card h3 { margin-top: 0; }

/* Small muted text */
.muted { color: #6b7280; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Auth guard ----------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to view your profile.")
    st.page_link("login.py", label="Go to Login")
    st.stop()

# ---------- Load current user ----------
users = get_users()
current_user = next((u for u in users if u["username"] == st.session_state.username), None)

st.title(f"Welcome to your profile, {st.session_state.username}!")
st.page_link("login.py", label="Back to Login Page")
st.divider()

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Edit Your Information")

    # Prepare defaults
    first_name_default = (current_user or {}).get("firstName", "")
    last_name_default  = (current_user or {}).get("lastName", "")
    today = date.today()
    min_date = date(today.year - 100, today.month, today.day)

    dob_str = (current_user or {}).get("dob")
    if dob_str:
        try:
            dob_default = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            dob_default = date(today.year - 18, today.month, today.day)
    else:
        dob_default = date(today.year - 18, today.month, today.day)

    # ---- Form
    with st.form("profile_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=first_name_default, placeholder="Fatma")
        with col2:
            last_name  = st.text_input("Last Name", value=last_name_default, placeholder="Alkendi")

        date_of_birth = st.date_input(
            "Date of Birth",
            value=dob_default,
            min_value=min_date,
            max_value=today
        )

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            profile_data = {
                "firstName": first_name.strip(),
                "lastName": last_name.strip(),
                "dob": date_of_birth.strftime("%Y-%m-%d"),
            }

            if update_user_profile(st.session_state.username, profile_data):
                st.success("Profile updated successfully!")
                st.toast("Saved ✅", icon="✅")
                # Keep a local copy to display below
                st.session_state["last_saved_profile"] = profile_data
            else:
                st.error("Failed to update profile.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Saved summary card ----------
if st.session_state.get("last_saved_profile"):
    saved = st.session_state["last_saved_profile"]
    st.markdown("#### Saved Profile")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.write("**First Name**")
            st.write(saved["firstName"] or "—")
            st.write("**Date of Birth**")
            st.write(saved["dob"] or "—")
        with c2:
            st.write("**Last Name**")
            st.write(saved["lastName"] or "—")
            st.write("**Username**")
            st.write(st.session_state.username)
        st.markdown('<span class="muted">These values reflect your latest save.</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- Logout ----------
colL, colR = st.columns([1, 2])
with colL:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("You have been successfully logged out.")
        st.switch_page("login.py")
