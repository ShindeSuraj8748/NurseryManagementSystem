from datetime import datetime
from app.database import db


class Variety(db.Model):

    __tablename__ = "varieties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    plant_id = db.Column(
        db.Integer,
        db.ForeignKey("plants.id"),
        nullable=False
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    days_to_ready = db.Column(
        db.Integer,
        nullable=False,
        default=25
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    plant = db.relationship(
        "Plant",
        back_populates="varieties"
    )

    company = db.relationship(
        "Company",
        back_populates="varieties"
    )