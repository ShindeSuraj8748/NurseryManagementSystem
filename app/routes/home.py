from flask import Blueprint, render_template
from sqlalchemy import func

from app.models import Plant
from app.database import db

main = Blueprint("main", __name__)


@main.route("/")
def home():

    total_plants = Plant.query.count()

    total_quantity = db.session.query(
        func.sum(Plant.quantity)
    ).scalar() or 0

    total_categories = db.session.query(
        Plant.category
    ).distinct().count()

    low_stock = Plant.query.filter(
        Plant.quantity < 10
    ).count()

    return render_template(
        "index.html",
        total_plants=total_plants,
        total_quantity=total_quantity,
        total_categories=total_categories,
        low_stock=low_stock,
    )