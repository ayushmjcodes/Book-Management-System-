"""
Application entry point.

Uses the "application factory" pattern (create_app) so the app can be
imported cleanly by seed_data.py, test scripts, or a production WSGI
server, without side effects happening just from importing this file.
"""

from flask import Flask, jsonify, redirect, request, url_for
from flask_login import LoginManager

from config import Config
from database.db import db
from models.user import User

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Wire up extensions to this app instance.
    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints here (not at module top) to avoid circular imports,
    # since routes import models, which import db from this same app setup.
    from routes.auth_routes import auth_bp
    from routes.category_routes import category_bp
    from routes.note_routes import note_bp
    from routes.page_routes import pages_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(note_bp, url_prefix="/api/notes")
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        # API calls should get a clean 401 JSON response (so fetch() can
        # handle it), while page loads should be redirected to the login
        # page like a normal website.
        if request.path.startswith("/api/"):
            return jsonify({"error": "Authentication required. Please log in."}), 401
        return redirect(url_for("pages.login_page"))

    @app.errorhandler(404)
    def not_found(_e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found."}), 404
        return redirect(url_for("pages.index"))

    @app.errorhandler(500)
    def server_error(_e):
        db.session.rollback()
        return jsonify({"error": "Internal server error. Please try again."}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
