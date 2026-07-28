from datetime import datetime
from app.database import db


class TraySize(db.Model):

    __tablename__ = "tray_sizes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    plant_count = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    batches = db.relationship(
        "PlantBatch",
        back_populates="tray"
    )