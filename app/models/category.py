from datetime import datetime
from app.database import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    plants = db.relationship(
        "Plant",
        back_populates="category_obj"
    )