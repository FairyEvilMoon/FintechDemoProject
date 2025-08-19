import json
import streamlit as st
import hashlib

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