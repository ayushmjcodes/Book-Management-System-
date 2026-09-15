"""
User model.

Represents a registered account. Passwords are never stored as plain
text - only a salted hash (via Werkzeug's generate_password_hash,
which uses PBKDF2-SHA256) is kept in the database.
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Deleting a user also deletes all of their notes and categories.
    notes = db.relationship(
        "Note", backref="author", lazy=True, cascade="all, delete-orphan"
    )
    categories = db.relationship(
        "Category", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        """Hashes and stores the given plain-text password."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """Verifies a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        """Safe representation of the user for JSON responses (no password)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.username}>"
