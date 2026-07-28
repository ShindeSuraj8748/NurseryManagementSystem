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
from flask import jsonify
from app.models import Variety
from app.models import TraySize     

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

    tray_sizes = TraySize.query.order_by(
        TraySize.plant_count
    ).all()

    if request.method == "POST":

        plant_id = int(request.form["plant_id"])

        variety_id = int(request.form["variety_id"])

        tray_size_id = int(request.form["tray_size_id"])

        number_of_trays = int(
            request.form["number_of_trays"]
        )

        sowing_date = datetime.strptime(
            request.form["sowing_date"],
            "%Y-%m-%d"
        ).date()

        remarks = request.form["remarks"]

        variety = Variety.query.get_or_404(
            variety_id
        )

        tray = TraySize.query.get_or_404(
            tray_size_id
        )

        estimated_plants = (
            tray.plant_count *
            number_of_trays
        )

        from datetime import timedelta

        ready_date = (
            sowing_date +
            timedelta(days=variety.days_to_ready)
        )

        batch = PlantBatch(

            plant_id=plant_id,

            variety_id=variety_id,

            tray_size_id=tray_size_id,

            number_of_trays=number_of_trays,

            estimated_plants=estimated_plants,

            sowing_date=sowing_date,

            ready_date=ready_date,

            remarks=remarks

        )

        db.session.add(batch)

        db.session.commit()

        flash(
            "Production Batch created successfully.",
            "success"
        )

        return redirect(
            url_for("batches.batch_list")
        )

    return render_template(
        "batches/add.html",
        plants=plants,
        tray_sizes=tray_sizes
    )

# -----------------------------
# API
# -----------------------------

@batches.route("/api/varieties/<int:plant_id>")
def get_varieties(plant_id):

    varieties = (
        Variety.query
        .filter_by(plant_id=plant_id)
        .order_by(Variety.name)
        .all()
    )

    return jsonify([
        {
            "id": v.id,
            "name": v.name
        }
        for v in varieties
    ])