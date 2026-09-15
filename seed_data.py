"""
One-time database setup and demo-data script.

Run with:  python seed_data.py

This creates all tables (if they don't already exist) and, if the
database is empty, inserts a demo user with a few sample notes so you
can log in and try the app immediately.
"""

from app import create_app
from database.db import db
from models.category import Category
from models.note import Note
from models.user import User

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo1234"

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created (or already existed).")

    if User.query.filter_by(email=DEMO_EMAIL).first():
        print("Demo data already exists - skipping seed.")
    else:
        demo_user = User(username="demo", email=DEMO_EMAIL)
        demo_user.set_password(DEMO_PASSWORD)
        db.session.add(demo_user)
        db.session.commit()

        work = Category(name="Work", user_id=demo_user.id)
        personal = Category(name="Personal", user_id=demo_user.id)
        db.session.add_all([work, personal])
        db.session.commit()

        notes = [
            Note(
                title="Welcome to NotesApp!",
                content=(
                    "This is your first note. Try pinning it, marking it as a "
                    "favorite, editing it, or deleting it from the dashboard."
                ),
                user_id=demo_user.id,
                is_pinned=True,
            ),
            Note(
                title="Grocery List",
                content="Milk, eggs, bread, coffee, spinach.",
                user_id=demo_user.id,
                category_id=personal.id,
            ),
            Note(
                title="Finish Flask backend",
                content="Implement remaining API routes and test authentication flow.",
                user_id=demo_user.id,
                category_id=work.id,
                is_favorite=True,
            ),
        ]
        db.session.add_all(notes)
        db.session.commit()

        print("Demo data created.")
        print(f"  Log in with -> email: {DEMO_EMAIL}  password: {DEMO_PASSWORD}")
