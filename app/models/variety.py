from datetime import datetime
from app.database import db


class Variety(db.Model):
    __tablename__ = "varieties"

    id = db.Column(db.Integer, primary_key=True)

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

    name = db.Column(
        db.String(100),
        nullable=False
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

    batches = db.relationship(
        "PlantBatch",
        back_populates="variety"
    )