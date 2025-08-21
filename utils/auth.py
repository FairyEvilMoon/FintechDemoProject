import json
import streamlit as st
import hashlib
from datetime import date

def get_users():
    """Reads user data from the JSON file."""
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    """Saves user data to the JSON file."""
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verifies a password against a hashed password."""
    return hash_password(password) == hashed_password

def update_user_profile(username, profile_data):
    """Updates the profile information for a specific user."""
    users = get_users()
    user_found = False
    for user in users:
        if user["username"] == username:
            user.update(profile_data)
            user_found = True
            break
    if user_found:
        save_users(users)
        return True
    return False