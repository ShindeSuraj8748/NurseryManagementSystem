from app.database import db
from datetime import datetime


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(50), nullable=False)

    price = db.Column(db.Numeric(10, 2), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=0)

    image = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    