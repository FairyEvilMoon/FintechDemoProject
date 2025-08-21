import streamlit as st
from utils.auth import get_users, update_user_profile
from datetime import datetime, date
import os
from PIL import Image
import base64

st.set_page_config(page_title="User Profile", page_icon="👤", layout="centered")

# ---------- Constants and Setup ----------
AVATAR_DIR = "assets/avatars"
if not os.path.exists(AVATAR_DIR):
    os.makedirs(AVATAR_DIR)

# ---------- Helper Function for Encoding Image ----------
def get_image_as_base64(path):
    """Encodes a local image file to a base64 string for display."""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except (FileNotFoundError, IOError):
        # This can happen if the path is saved but the file is deleted
        return None

# ---------- Custom CSS for Styling ----------
st.markdown("""
<style>
.main > div { max-width: 820px; margin: auto; }

/* Styles for the circular avatar display */
.avatar-display {
    width: 128px;
    height: 128px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #eee;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* Vertically center the content in the uploader column */
.uploader-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}
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

# ---------- Title ----------
st.title(f"Welcome to your profile, {st.session_state.username}!")
st.markdown("---")


# ---------- NEW INTERACTIVE AVATAR SECTION ----------
col1, col2 = st.columns([1, 2])
with col1:
    avatar_path = (current_user or {}).get("avatar")
    b64_image = get_image_as_base64(avatar_path) if avatar_path else None

    if b64_image:
        st.markdown(f'<img src="data:image/png;base64,{b64_image}" class="avatar-display">', unsafe_allow_html=True)
    else:
        # Default placeholder avatar
        st.markdown('<img src="https://static.streamlit.io/examples/cat.jpg" class="avatar-display">', unsafe_allow_html=True)

# The file uploader is now placed here, visually next to the avatar
with col2:
    st.markdown('<div class="uploader-container">', unsafe_allow_html=True)
    avatar_upload = st.file_uploader(
        "Upload a new photo",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed", # Hides the label to make it cleaner
        help="Upload a new picture to serve as your avatar."
    )
    st.markdown("To change your avatar, upload a new image and click 'Save Changes' below.")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- PROFILE EDIT FORM ----------
with st.container():
    st.markdown("### Edit Your Information")

    # Prepare defaults from user data
    first_name_default = (current_user or {}).get("firstName", "")
    last_name_default  = (current_user or {}).get("lastName", "")
    today = date.today()
    min_date = date(today.year - 100, today.month, today.day)
    dob_default = date(today.year - 18, today.month, today.day)

    dob_str = (current_user or {}).get("dob")
    if dob_str:
        try:
            dob_default = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            pass

    with st.form("profile_form", clear_on_submit=False):
        first_name = st.text_input("First Name", value=first_name_default)
        last_name  = st.text_input("Last Name", value=last_name_default)
        date_of_birth = st.date_input("Date of Birth", value=dob_default, min_value=min_date, max_value=today)

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            # Prepare data to be saved
            profile_data = {
                "firstName": first_name.strip(),
                "lastName": last_name.strip(),
                "dob": date_of_birth.strftime("%Y-%m-%d"),
            }
            has_changes = False

            # --- ROBUST FILE HANDLING ---
            # Check if a new avatar was uploaded in the section above
            if avatar_upload is not None:
                try:
                    img = Image.open(avatar_upload)
                    img = img.convert("RGB") # Standardize image format

                    # Save the new avatar with a consistent name
                    new_avatar_filename = f"{st.session_state.username}.png"
                    new_avatar_path = os.path.join(AVATAR_DIR, new_avatar_filename)
                    img.save(new_avatar_path, "PNG")

                    # Add the new avatar path to the data to be saved
                    profile_data["avatar"] = new_avatar_path
                    has_changes = True
                    st.toast("New avatar is ready to be saved!", icon="🖼️")
                except Exception as e:
                    st.error(f"Error processing avatar: {e}")
                    st.stop() # Stop execution if image processing fails

            # Update the user's profile in the JSON file
            if update_user_profile(st.session_state.username, profile_data):
                st.success("Profile updated successfully!")
                st.toast("Saved!", icon="✅")
                # Rerun the script to show all changes immediately
                st.rerun()
            else:
                st.error("Failed to save your profile. Please try again.")


# ---------- Logout Buttons ----------
st.markdown("---")
colL, colR = st.columns(2)
with colL:
    if st.button("Back to Home Page", use_container_width=True):
        st.switch_page("login.py")
with colR:
    if st.button("Logout", type="secondary", use_container_width=True):
        st.session_state.clear() # Clear the session for a clean logout
        st.switch_page("login.py")