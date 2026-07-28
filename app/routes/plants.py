from flask import Blueprint, render_template, request, redirect , url_for
from app.database import db
from app.models import Plant

plants = Blueprint("plants", __name__)

@plants.route("/plants/add", methods=["GET", "POST"])
def add_plant():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        
        new_plant = Plant(
    name=name,
    category=category,
    price=price,
    quantity=quantity
)
        db.session.add(new_plant)
        db.session.commit()
        return redirect(url_for("plants.plant_list"))

    return render_template("add_plant.html")

@plants.route("/plants")
def plant_list():
    plants_list = Plant.query.all()
    return render_template("plant_list.html", plants=plants_list)

@plants.route("/plants/edit/<int:id>",methods=["GET","POST"])
def edit_plant(id):
    plant = Plant.query.get_or_404(id)
    
    if request.method == "POST":
        plant.name = request.form["name"]
        plant.category = request.form["category"]
        plant.price = request.form["price"]
        plant.quantity = request.form["quantity"]

        db.session.commit()

        return redirect(url_for("plants.plant_list"))

    return render_template("edit_plant.html",plant=plant)

@plants.route("/plants/delete/<int:id>")
def delete_plant(id):
    plant = Plant.query.get_or_404(id)

    db.session.delete(plant)
    db.session.commit()

    return redirect(url_for("plants.plant_list"))
