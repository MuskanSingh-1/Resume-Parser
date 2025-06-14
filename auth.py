import re
import hashlib
from db import add_user, get_user_by_email

# --------- Utility Functions ---------

# Hash the password using SHA256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Verify input password with stored hashed password
def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash

# Validate email format
def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Validate password strength
def is_strong_password(password: str) -> bool:
    return (
        len(password) >= 6 and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        any(char.isdigit() for char in password)
    )

# --------- Sign-up & Sign-in Handlers ---------

# Sign-up handler: returns (success, message)
def handle_signup(name: str, email: str, password: str) -> tuple[bool, str]:
    if not name.strip():
        return False, "Name cannot be empty."

    if not is_valid_email(email):
        return False, "Invalid email format."

    if not is_strong_password(password):
        return False, "Password must be at least 6 characters, and contain uppercase, lowercase, and a number."

    hashed_pw = hash_password(password)
    success = add_user(name, email, hashed_pw)

    if success:
        return True, "User registered successfully!"
    else:
        return False, "Email already exists."

# Sign-in handler: returns (success, user_data/message)
def handle_signin(email: str, password: str) -> tuple[bool, str | tuple]:
    if not is_valid_email(email):
        return False, "Invalid email format."

    user = get_user_by_email(email)
    if not user:
        return False, "User not found. Please sign up first."

    user_id, name, email_stored, password_hash = user
    if not verify_password(password, password_hash):
        return False, "Incorrect password."

    return True, user  # successful login returns full user tuple