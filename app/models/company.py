from datetime import datetime
from app.database import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    varieties = db.relationship(
        "Variety",
        back_populates="company",
        cascade="all, delete-orphan"
    )