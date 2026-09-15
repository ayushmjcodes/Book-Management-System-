"""
Page (view) routes: serve the actual HTML pages via Jinja templates.

These are separate from the /api/* routes. Pages just render a
template shell; the templates then use JavaScript (fetch) to talk to
the /api/* endpoints and fill in real data. This keeps a clean split
between "what the browser loads" and "the data it fetches after".
"""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("pages.dashboard_page"))
    return redirect(url_for("pages.login_page"))


@pages_bp.route("/login")
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("pages.dashboard_page"))
    return render_template("login.html")


@pages_bp.route("/register")
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("pages.dashboard_page"))
    return render_template("register.html")


@pages_bp.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html", username=current_user.username)


@pages_bp.route("/notes/create")
@login_required
def create_note_page():
    return render_template("create_note.html", username=current_user.username)


@pages_bp.route("/notes/<int:note_id>/edit")
@login_required
def edit_note_page(note_id):
    return render_template(
        "edit_note.html", note_id=note_id, username=current_user.username
    )


@pages_bp.route("/notes/<int:note_id>")
@login_required
def view_note_page(note_id):
    return render_template(
        "view_note.html", note_id=note_id, username=current_user.username
    )
