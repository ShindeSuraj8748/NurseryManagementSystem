from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app.database import db
from app.models import Variety, Plant, Company

variety = Blueprint("variety", __name__)


@variety.route("/varieties")
def variety_list():

    varieties = (
        Variety.query
        .order_by(Variety.name)
        .all()
    )

    return render_template(
        "varieties/list.html",
        varieties=varieties
    )


@variety.route(
    "/varieties/add",
    methods=["GET", "POST"]
)
def add_variety():

    plants = Plant.query.order_by(Plant.name).all()
    companies = Company.query.order_by(Company.name).all()

    if request.method == "POST":

        name = request.form["name"].strip()

        plant_id = int(request.form["plant_id"])

        company_id = int(request.form["company_id"])

        days_to_ready = int(
            request.form["days_to_ready"]
        )

        exists = Variety.query.filter_by(
            name=name,
            plant_id=plant_id,
            company_id=company_id
        ).first()

        if exists:

            flash(
                "Variety already exists.",
                "warning"
            )

            return redirect(request.url)

        variety = Variety(

            name=name,

            plant_id=plant_id,

            company_id=company_id,

            days_to_ready=days_to_ready

        )

        db.session.add(variety)

        db.session.commit()

        flash(
            "Variety added successfully.",
            "success"
        )

        return redirect(
            url_for("variety.variety_list")
        )

    return render_template(
        "varieties/add.html",
        plants=plants,
        companies=companies
    )

@variety.route(
    "/varieties/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_variety(id):

    variety = Variety.query.get_or_404(id)

    if request.method == "POST":

        variety.name = request.form["name"]
        variety.plant_id = request.form["plant_id"]
        variety.company_id = request.form["company_id"]
        variety.days_to_ready = request.form["days_to_ready"]

        db.session.commit()

        flash(
            "Variety updated successfully.",
            "success"
        )

        return redirect(
            url_for("variety.variety_list")
        )

    return render_template(
        "varieties/edit.html",
        variety=variety,
        plants=Plant.query.order_by(Plant.name).all(),
        companies=Company.query.order_by(Company.name).all()
    )


@variety.route("/varieties/delete/<int:id>")
def delete_variety(id):

    variety = Variety.query.get_or_404(id)

    db.session.delete(variety)
    db.session.commit()

    flash(
        "Variety deleted successfully.",
        "danger"
    )

    return redirect(
        url_for("variety.variety_list")
    )