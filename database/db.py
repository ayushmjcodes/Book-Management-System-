"""
Central SQLAlchemy instance.

This is defined in its own module (separate from app.py) so that
models/*.py can import `db` without causing a circular import with
the application factory in app.py.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
