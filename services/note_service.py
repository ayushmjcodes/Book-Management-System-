"""
Note business logic: search/filter, CRUD, and pin/favorite toggling.

Every function here takes the current user's id and scopes its query
to that user - this is what guarantees a user can never read, edit,
or delete another user's notes, even if they guess a valid note id.
"""

from database.db import db
from models.category import Category
from models.note import Note


class NoteError(Exception):
    """Raised for any note operation failure, with a user-friendly message."""


def get_notes_for_user(user_id, search=None, category_id=None, favorite=None):
    """Returns the current user's notes, optionally filtered, pinned notes first."""
    query = Note.query.filter_by(user_id=user_id)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            db.or_(Note.title.ilike(like_pattern), Note.content.ilike(like_pattern))
        )

    if category_id:
        query = query.filter_by(category_id=category_id)

    if favorite is not None:
        query = query.filter_by(is_favorite=favorite)

    # Pinned notes always show first, then most-recently-updated first.
    return query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()


def get_note_or_404(note_id, user_id):
    """Fetches a single note, ensuring it belongs to the requesting user."""
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        raise NoteError("Note not found.")
    return note


def _validate_category(category_id, user_id):
    """Ensures a category_id (if provided) actually belongs to this user."""
    if category_id in (None, "", 0, "0"):
        return None
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        raise NoteError("Invalid category.")
    return category.id


def create_note(user_id, title, content=None, category_id=None):
    if not title or not title.strip():
        raise NoteError("Title is required.")
    if len(title) > 200:
        raise NoteError("Title must be under 200 characters.")

    validated_category_id = _validate_category(category_id, user_id)

    note = Note(
        title=title.strip(),
        content=(content or "").strip(),
        user_id=user_id,
        category_id=validated_category_id,
    )
    db.session.add(note)
    db.session.commit()
    return note


def update_note(note_id, user_id, title=None, content=None, category_id=None, **_ignored):
    """
    Updates a note from a full form submission (the edit page always
    sends title, content, and category_id together). category_id is
    replaced outright - including being cleared back to "no category" -
    rather than only updated when truthy, so unchecking a note's
    category actually removes it instead of being silently ignored.
    """
    note = get_note_or_404(note_id, user_id)

    if title is None or not title.strip():
        raise NoteError("Title cannot be empty.")
    note.title = title.strip()

    note.content = (content or "").strip()
    note.category_id = _validate_category(category_id, user_id)

    db.session.commit()
    return note


def delete_note(note_id, user_id):
    note = get_note_or_404(note_id, user_id)
    db.session.delete(note)
    db.session.commit()


def toggle_pin(note_id, user_id):
    note = get_note_or_404(note_id, user_id)
    note.is_pinned = not note.is_pinned
    db.session.commit()
    return note


def toggle_favorite(note_id, user_id):
    note = get_note_or_404(note_id, user_id)
    note.is_favorite = not note.is_favorite
    db.session.commit()
    return note
