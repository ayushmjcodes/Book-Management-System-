"""
Authentication business logic.

Keeping this logic out of routes/auth_routes.py keeps the route
functions thin (just handling HTTP concerns) and makes the actual
rules easy to find, read, and reuse or test independently.
"""

import re

from database.db import db
from models.user import User


class AuthError(Exception):
    """Raised for any registration/login failure with a user-friendly message."""


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register_user(username, email, password):
    """Validates input and creates a new user account with a hashed password."""
    if not username or len(username) < 3:
        raise AuthError("Username must be at least 3 characters long.")
    if len(username) > 50:
        raise AuthError("Username must be under 50 characters.")
    if not email or not EMAIL_REGEX.match(email):
        raise AuthError("Please provide a valid email address.")
    if not password or len(password) < 6:
        raise AuthError("Password must be at least 6 characters long.")

    if User.query.filter_by(username=username).first():
        raise AuthError("That username is already taken.")
    if User.query.filter_by(email=email).first():
        raise AuthError("An account with that email already exists.")

    user = User(username=username, email=email)
    user.set_password(password)  # Hashes before storing - never save plain text.
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email, password):
    """Checks credentials and returns the matching user, or raises AuthError."""
    if not email or not password:
        raise AuthError("Email and password are required.")

    user = User.query.filter_by(email=email).first()

    # Deliberately use the same error message whether the email doesn't
    # exist or the password is wrong, so we don't reveal which emails
    # are registered to an attacker.
    if not user or not user.check_password(password):
        raise AuthError("Invalid email or password.")

    return user
