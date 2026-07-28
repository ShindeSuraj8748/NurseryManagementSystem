from datetime import datetime
from app.database import db


class PlantBatch(db.Model):
    __tablename__ = "plant_batches"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    plant_id = db.Column(
        db.Integer,
        db.ForeignKey("plants.id"),
        nullable=False
    )

    # Temporary
    # Later this will become variety_id
    variety = db.Column(
        db.String(100),
        nullable=False
    )

    tray_size_id = db.Column(
        db.Integer,
        db.ForeignKey("tray_sizes.id"),
        nullable=False
    )

    plants_per_tray = db.Column(
        db.Integer,
        nullable=False
    )

    estimated_plants = db.Column(
        db.Integer,
        nullable=False
    )

    sowing_date = db.Column(
        db.Date,
        nullable=False
    )

    ready_date = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(30),
        default="Growing"
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # -------------------------
    # Relationships
    # -------------------------

    plant = db.relationship(
        "Plant",
        back_populates="batches"
    )

    tray = db.relationship(
        "TraySize",
        back_populates="batches"
    )