"""
Application configuration.

All values are read from environment variables (loaded from a .env file
in development) so that secrets and environment-specific settings are
never hard-coded into the source code.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file into the environment, if one exists.
load_dotenv()


class Config:
    # Used by Flask to cryptographically sign session cookies.
    # MUST be overridden with a real secret in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLAlchemy connection string for PostgreSQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/notes_db",
    )

    # Disables a SQLAlchemy feature we don't need; avoids extra overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie security settings.
    SESSION_COOKIE_HTTPONLY = True   # JavaScript cannot read the cookie.
    SESSION_COOKIE_SAMESITE = "Lax"  # Basic protection against CSRF.

    # How long a "remember me" session stays valid, in seconds.
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("SESSION_LIFETIME_SECONDS", 86400))
