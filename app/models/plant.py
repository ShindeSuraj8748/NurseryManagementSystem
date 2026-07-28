from datetime import datetime
from app.database import db


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category_obj = db.relationship(
        "Category",
        back_populates="plants"
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    image = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    batches = db.relationship(
        "PlantBatch",
        back_populates="plant",
        cascade="all, delete-orphan"
    )

    @property
    def stock(self):
        return sum(
            batch.estimated_plants
            for batch in self.batches
            if batch.status != "Sold"
        )

    @property
    def category(self):
        if self.category_obj:
            return self.category_obj.name
        return ""