from datetime import datetime
from app.database import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_no = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    advance_amount = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    total_amount = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    balance_amount = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    customer = db.relationship(
        "Customer",
        back_populates="bookings"
    )

    items = db.relationship(
        "BookingItem",
        back_populates="booking",
        cascade="all, delete-orphan"
    )