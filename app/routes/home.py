from flask import Blueprint, render_template
from sqlalchemy import func

from app.database import db
from app.models import Plant
from app.models import Category
from app.models import PlantBatch

main = Blueprint("main", __name__)


@main.route("/")
def home():

    # Total plant types
    total_plants = Plant.query.count()

    # Total available stock from all batches
    total_quantity = (
        db.session.query(
            func.coalesce(func.sum(PlantBatch.estimated_plants), 0)
        ).scalar()
    )

    # Total categories
    total_categories = Category.query.count()

    # Plants having stock less than 10
    low_stock = 0

    plants = Plant.query.all()

    for plant in plants:
        if plant.stock < 10:
            low_stock += 1

    return render_template(
        "index.html",
        total_plants=total_plants,
        total_quantity=total_quantity,
        total_categories=total_categories,
        low_stock=low_stock,
    )