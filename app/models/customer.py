from datetime import datetime
from app.database import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    mobile = db.Column(
        db.String(15),
        nullable=False
    )

    village = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
    bookings = db.relationship(
    "Booking",
    back_populates="customer",
    cascade="all, delete-orphan"
)