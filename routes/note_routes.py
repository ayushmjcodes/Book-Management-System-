"""
Note API endpoints: /api/notes/*

Every route is protected with @login_required, and every service call
is scoped to current_user.id, so a logged-in user can only ever see
or modify their own notes.
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from services.note_service import (
    NoteError,
    create_note,
    delete_note,
    get_note_or_404,
    get_notes_for_user,
    toggle_favorite,
    toggle_pin,
    update_note,
)

note_bp = Blueprint("notes", __name__)


def _error_status(message):
    """404 for 'not found' style errors, 400 for everything else (bad input)."""
    return 404 if "not found" in message.lower() else 400


@note_bp.route("", methods=["GET"])
@login_required
def list_notes():
    search = request.args.get("search", "").strip() or None
    category_id = request.args.get("category_id", type=int)

    favorite_param = request.args.get("favorite")
    favorite = True if favorite_param == "true" else None

    notes = get_notes_for_user(
        current_user.id, search=search, category_id=category_id, favorite=favorite
    )
    return jsonify({"notes": [n.to_dict() for n in notes]}), 200


@note_bp.route("", methods=["POST"])
@login_required
def add_note():
    data = request.get_json(silent=True) or {}
    try:
        note = create_note(
            current_user.id,
            title=data.get("title", ""),
            content=data.get("content", ""),
            category_id=data.get("category_id"),
        )
    except NoteError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Note created.", "note": note.to_dict()}), 201


@note_bp.route("/<int:note_id>", methods=["GET"])
@login_required
def get_note(note_id):
    try:
        note = get_note_or_404(note_id, current_user.id)
    except NoteError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"note": note.to_dict()}), 200


@note_bp.route("/<int:note_id>", methods=["PUT"])
@login_required
def edit_note(note_id):
    data = request.get_json(silent=True) or {}
    try:
        note = update_note(
            note_id,
            current_user.id,
            title=data.get("title"),
            content=data.get("content"),
            category_id=data.get("category_id"),
        )
    except NoteError as e:
        return jsonify({"error": str(e)}), _error_status(str(e))
    return jsonify({"message": "Note updated.", "note": note.to_dict()}), 200


@note_bp.route("/<int:note_id>", methods=["DELETE"])
@login_required
def remove_note(note_id):
    try:
        delete_note(note_id, current_user.id)
    except NoteError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Note deleted."}), 200


@note_bp.route("/<int:note_id>/pin", methods=["PATCH"])
@login_required
def pin_note(note_id):
    try:
        note = toggle_pin(note_id, current_user.id)
    except NoteError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Pin status updated.", "note": note.to_dict()}), 200


@note_bp.route("/<int:note_id>/favorite", methods=["PATCH"])
@login_required
def favorite_note(note_id):
    try:
        note = toggle_favorite(note_id, current_user.id)
    except NoteError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Favorite status updated.", "note": note.to_dict()}), 200
