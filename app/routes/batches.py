from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app.database import db
from app.models import Plant, PlantBatch
from datetime import datetime

batches = Blueprint(
    "batches",
    __name__,
)


@batches.route("/batches")
def batch_list():

    batches_list = (
        PlantBatch.query
        .order_by(PlantBatch.id.desc())
        .all()
    )

    return render_template(
        "batches/list.html",
        batches=batches_list,
    )


@batches.route("/batches/add", methods=["GET", "POST"])
def add_batch():

    plants = Plant.query.order_by(
        Plant.name
    ).all()

    if request.method == "POST":

        plant_id = request.form["plant_id"]

        variety = request.form["variety"]

        tray_size = int(
            request.form["tray_size"]
        )

        tray_count = int(
            request.form["tray_count"]
        )

        estimated_plants = (
            tray_size * tray_count
        )

        sowing_date = datetime.strptime(
            request.form["sowing_date"],
            "%Y-%m-%d"
        ).date()

        ready_date = datetime.strptime(
            request.form["ready_date"],
            "%Y-%m-%d"
        ).date()

        batch = PlantBatch(
            plant_id=plant_id,
            variety=variety,
            tray_size=tray_size,
            tray_count=tray_count,
            estimated_plants=estimated_plants,
            sowing_date=sowing_date,
            ready_date=ready_date,
        )

        db.session.add(batch)
        db.session.commit()

        flash(
            "Batch added successfully.",
            "success"
        )

        return redirect(
            url_for("batches.batch_list")
        )

    return render_template(
        "batches/add.html",
        plants=plants,
    )