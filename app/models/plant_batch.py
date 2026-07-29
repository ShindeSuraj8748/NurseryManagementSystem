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

    variety_id = db.Column(
    db.Integer,
    db.ForeignKey("varieties.id"),
    nullable=False
)

    variety = db.relationship(
        "Variety"
    )

    tray_size_id = db.Column(
        db.Integer,
        db.ForeignKey("tray_sizes.id"),
        nullable=False
    )

    number_of_trays = db.Column(
    db.Integer,
    nullable=False
)

    estimated_plants = db.Column(
    db.Integer,
    nullable=False
)

    reserved_plants = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    sold_plants = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    damaged_plants = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    imported_plants = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    exported_plants = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    selling_price = db.Column(
        db.Numeric(10, 2),
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
    
    @property
    def physical_stock(self):
        return (
            self.estimated_plants
            + self.imported_plants
            - self.exported_plants
            - self.sold_plants
            - self.damaged_plants
        )

    @property
    def available_plants(self):
        return self.physical_stock - self.reserved_plants

    @property
    def shortage(self):
        if self.available_plants < 0:
            return abs(self.available_plants)
        return 0
        
    @property
    def batch_name(self):
        return f"{self.plant.name} - {self.variety.name} - Batch {self.id}"


    @property
    def current_price(self):
        return float(self.selling_price)