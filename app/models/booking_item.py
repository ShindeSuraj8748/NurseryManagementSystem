from app.database import db


class BookingItem(db.Model):
    __tablename__ = "booking_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False
    )

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("plant_batches.id"),
        nullable=False
    )

    # Snapshot fields
    plant_name = db.Column(
        db.String(100),
        nullable=False
    )

    variety_name = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    rate = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    booking = db.relationship(
        "Booking",
        back_populates="items"
    )

    batch = db.relationship(
        "PlantBatch"
    )