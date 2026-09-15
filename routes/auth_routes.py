"""
Authentication API endpoints: /api/auth/*

These return JSON and are called by static/js/auth.js using fetch().
"""

from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required, login_user, logout_user

from services.auth_service import AuthError, authenticate_user, register_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    try:
        user = register_user(
            username=(data.get("username") or "").strip(),
            email=(data.get("email") or "").strip().lower(),
            password=data.get("password") or "",
        )
    except AuthError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Registration successful.", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    try:
        user = authenticate_user(
            email=(data.get("email") or "").strip().lower(),
            password=data.get("password") or "",
        )
    except AuthError as e:
        return jsonify({"error": str(e)}), 401

    login_user(user, remember=True)
    session.permanent = True
    return jsonify({"message": "Login successful.", "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({"user": current_user.to_dict()}), 200
