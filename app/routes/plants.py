import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app.database import db
from app.models import Plant

plants = Blueprint("plants", __name__)

# ----------------------------
# Categories
# ----------------------------
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

# ----------------------------
# Allowed Image Types
# ----------------------------
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================================================
# ADD PLANT
# ==========================================================
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

            # Validate image type
            if not allowed_file(image.filename):
                flash(
                    "Only JPG, JPEG, PNG and WEBP images are allowed.",
                    "danger",
                )
                return redirect(request.url)

            filename = secure_filename(image.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"

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


# ==========================================================
# PLANT LIST
# ==========================================================
@plants.route("/plants")
def plant_list():

    search = request.args.get("search", "")

    if search:

        plants_list = (
            Plant.query.filter(
                or_(
                    Plant.name.ilike(f"%{search}%"),
                    Plant.category.ilike(f"%{search}%"),
                )
            )
            .order_by(Plant.id.desc())
            .all()
        )

    else:

        plants_list = (
            Plant.query.order_by(
                Plant.id.desc()
            ).all()
        )

    return render_template(
        "plant_list.html",
        plants=plants_list,
        search=search,
    )


# ==========================================================
# EDIT PLANT
# ==========================================================
@plants.route("/plants/edit/<int:id>", methods=["GET", "POST"])
def edit_plant(id):

    plant = Plant.query.get_or_404(id)

    if request.method == "POST":

        plant.name = request.form["name"]
        plant.category = request.form["category"]
        plant.price = request.form["price"]
        plant.quantity = request.form["quantity"]

        image = request.files.get("image")

        if image and image.filename:

            # Validate image
            if not allowed_file(image.filename):
                flash(
                    "Only JPG, JPEG, PNG and WEBP images are allowed.",
                    "danger",
                )
                return redirect(request.url)

            # Delete old image
            if plant.image:

                old_image = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    plant.image,
                )

                try:
                    if os.path.exists(old_image):
                        os.remove(old_image)
                except Exception as e:
                    print(f"Error deleting image: {e}")

            filename = secure_filename(image.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename,
                )
            )

            plant.image = filename

        db.session.commit()

        flash("Plant updated successfully!", "warning")

        return redirect(url_for("plants.plant_list"))

    return render_template(
        "edit_plant.html",
        plant=plant,
        categories=CATEGORIES,
    )


# ==========================================================
# DELETE PLANT
# ==========================================================
@plants.route("/plants/delete/<int:id>")
def delete_plant(id):

    plant = Plant.query.get_or_404(id)

    if plant.image:

        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            plant.image,
        )

        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error deleting image: {e}")

    db.session.delete(plant)
    db.session.commit()

    flash("Plant deleted successfully!", "danger")

    return redirect(url_for("plants.plant_list"))