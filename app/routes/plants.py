from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from app.database import db
from app.models import Plant

import os
from werkzeug.utils import secure_filename

plants = Blueprint("plants", __name__)

CATEGORIES = [
    "Flower",
    "Fruit",
    "Vegetable",
    "Medicinal",
    "Indoor",
    "Outdoor",
    "Decorative",
    "Tree",
]


@plants.route("/plants/add", methods=["GET", "POST"])
def add_plant():

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        image = request.files.get("image")

        filename = None

        if image and image.filename:
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename,
                )
            )

        new_plant = Plant(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            image=filename,
        )

        db.session.add(new_plant)
        db.session.commit()

        flash("Plant added successfully!", "success")

        return redirect(url_for("plants.plant_list"))

    return render_template(
        "add_plant.html",
        categories=CATEGORIES,
    )


@plants.route("/plants")
def plant_list():

    search = request.args.get("search", "")

    if search:
        plants_list = Plant.query.filter(
            Plant.name.ilike(f"%{search}%")
        ).all()
    else:
        plants_list = Plant.query.all()

    return render_template(
        "plant_list.html",
        plants=plants_list,
        search=search,
    )


@plants.route("/plants/edit/<int:id>", methods=["GET", "POST"])
def edit_plant(id):

    plant = Plant.query.get_or_404(id)

    if request.method == "POST":

        plant.name = request.form["name"]
        plant.category = request.form["category"]
        plant.price = request.form["price"]
        plant.quantity = request.form["quantity"]

        db.session.commit()

        flash("Plant updated successfully!", "warning")

        return redirect(url_for("plants.plant_list"))

    return render_template(
        "edit_plant.html",
        plant=plant,
        categories=CATEGORIES,
    )


@plants.route("/plants/delete/<int:id>")
def delete_plant(id):

    plant = Plant.query.get_or_404(id)

    db.session.delete(plant)
    db.session.commit()

    flash("Plant deleted successfully!", "danger")

    return redirect(url_for("plants.plant_list"))   