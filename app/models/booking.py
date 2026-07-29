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
    nullable=False,
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
    
    def calculate_totals(self):

        self.total_amount = sum(
            item.total_price
            for item in self.items
        )

        self.balance_amount = (
            self.total_amount
            - self.advance_amount
        )
        
    def complete(self):

        if self.status == "Completed":
            return

        self.status = "Completed"

        for item in self.items:

            batch = item.batch

            batch.reserved_plants = max(
                0,
                batch.reserved_plants - item.quantity
            )

            batch.sold_plants += item.quantity

        self.balance_amount = 0