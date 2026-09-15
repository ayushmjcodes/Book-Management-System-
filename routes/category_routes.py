"""
Category API endpoints: /api/categories/*
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from database.db import db
from models.category import Category

category_bp = Blueprint("categories", __name__)


@category_bp.route("", methods=["GET"])
@login_required
def list_categories():
    categories = (
        Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    )
    return jsonify({"categories": [c.to_dict() for c in categories]}), 200


@category_bp.route("", methods=["POST"])
@login_required
def add_category():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Category name is required."}), 400
    if len(name) > 50:
        return jsonify({"error": "Category name must be under 50 characters."}), 400

    exists = Category.query.filter_by(user_id=current_user.id, name=name).first()
    if exists:
        return jsonify({"error": "You already have a category with that name."}), 400

    category = Category(name=name, user_id=current_user.id)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Category created.", "category": category.to_dict()}), 201
