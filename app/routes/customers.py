from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from sqlalchemy import or_

from app.database import db
from app.models import Customer

customers = Blueprint(
    "customers",
    __name__,
)


# ==========================
# LIST
# ==========================

@customers.route("/customers")
def customer_list():

    search = request.args.get("search", "")

    if search:

        customers_list = (
            Customer.query.filter(
                or_(
                    Customer.name.ilike(f"%{search}%"),
                    Customer.mobile.ilike(f"%{search}%"),
                    Customer.village.ilike(f"%{search}%"),
                )
            )
            .order_by(Customer.id.desc())
            .all()
        )

    else:

        customers_list = (
            Customer.query
            .order_by(Customer.id.desc())
            .all()
        )

    return render_template(
        "customers/list.html",
        customers=customers_list,
        search=search,
    )


# ==========================
# ADD
# ==========================

@customers.route(
    "/customers/add",
    methods=["GET", "POST"]
)
def add_customer():

    if request.method == "POST":

        customer = Customer(

            name=request.form["name"],

            mobile=request.form["mobile"],

            village=request.form["village"],

            address=request.form["address"],

            remarks=request.form["remarks"]

        )

        db.session.add(customer)

        db.session.commit()

        flash(
            "Customer added successfully.",
            "success"
        )

        return redirect(
            url_for("customers.customer_list")
        )

    return render_template(
        "customers/add.html"
    )


# ==========================
# EDIT
# ==========================

@customers.route(
    "/customers/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_customer(id):

    customer = Customer.query.get_or_404(id)

    if request.method == "POST":

        customer.name = request.form["name"]
        customer.mobile = request.form["mobile"]
        customer.village = request.form["village"]
        customer.address = request.form["address"]
        customer.remarks = request.form["remarks"]

        db.session.commit()

        flash(
            "Customer updated successfully.",
            "success"
        )

        return redirect(
            url_for("customers.customer_list")
        )

    return render_template(
        "customers/edit.html",
        customer=customer
    )


# ==========================
# DELETE
# ==========================

@customers.route(
    "/customers/delete/<int:id>"
)
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)

    db.session.commit()

    flash(
        "Customer deleted successfully.",
        "danger"
    )

    return redirect(
        url_for("customers.customer_list")
    )