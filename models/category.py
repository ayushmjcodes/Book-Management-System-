"""
Category model.

Categories belong to a single user (each user manages their own set
of categories, e.g. "Work", "Personal"). A note may optionally belong
to one category.
"""

from database.db import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # A single user cannot have two categories with the same name.
    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_user_category_name"),
    )

    notes = db.relationship("Note", backref="category", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f"<Category {self.name}>"
