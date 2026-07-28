import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database import db
from app.models import TraySize

tray = Blueprint(
    "tray",
    __name__
)


# ==========================
# LIST
# ==========================

@tray.route("/tray-sizes")
def tray_list():

    search = request.args.get("search", "")

    if search:

        trays = TraySize.query.filter(
            TraySize.name.ilike(f"%{search}%")
        ).all()

    else:

        trays = TraySize.query.order_by(
            TraySize.id.desc()
        ).all()

    return render_template(
        "tray_sizes/list.html",
        trays=trays,
        search=search
    )


# ==========================
# ADD
# ==========================

@tray.route(
    "/tray-sizes/add",
    methods=["GET", "POST"]
)
def add_tray():

    if request.method == "POST":

        name = request.form["name"]

        rows = int(request.form["rows"])

        columns = int(request.form["columns"])

        status = request.form["status"]

        if TraySize.query.filter_by(name=name).first():

            flash(
                "Tray already exists.",
                "warning"
            )

            return redirect(request.url)

        plants_per_tray = rows * columns

        tray_size = TraySize(

            name=name,

            rows=rows,

            columns=columns,

            plants_per_tray=plants_per_tray,

            status=status
        )

        db.session.add(tray_size)

        db.session.commit()

        flash(
            "Tray added successfully.",
            "success"
        )

        return redirect(
            url_for("tray.tray_list")
        )

    return render_template(
        "tray_sizes/add.html"
    )


# ==========================
# EDIT
# ==========================

@tray.route(
    "/tray-sizes/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_tray(id):

    tray_size = TraySize.query.get_or_404(id)

    if request.method == "POST":

        tray_size.name = request.form["name"]

        tray_size.rows = int(
            request.form["rows"]
        )

        tray_size.columns = int(
            request.form["columns"]
        )

        tray_size.status = request.form["status"]

        tray_size.plants_per_tray = (
            tray_size.rows *
            tray_size.columns
        )

        db.session.commit()

        flash(
            "Tray updated successfully.",
            "success"
        )

        return redirect(
            url_for("tray.tray_list")
        )

    return render_template(
        "tray_sizes/edit.html",
        tray=tray_size
    )


# ==========================
# DELETE
# ==========================

@tray.route(
    "/tray-sizes/delete/<int:id>"
)
def delete_tray(id):

    tray_size = TraySize.query.get_or_404(id)

    db.session.delete(tray_size)

    db.session.commit()

    flash(
        "Tray deleted successfully.",
        "danger"
    )

    return redirect(
        url_for("tray.tray_list")
    )