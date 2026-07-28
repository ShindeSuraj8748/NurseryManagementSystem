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
from app.models import Company

company = Blueprint(
    "company",
    __name__,
)


# ==========================================================
# COMPANY LIST
# ==========================================================
@company.route("/companies")
def company_list():

    search = request.args.get("search", "")

    if search:

        companies = (
            Company.query.filter(
                Company.name.ilike(f"%{search}%")
            )
            .order_by(Company.name)
            .all()
        )

    else:

        companies = (
            Company.query
            .order_by(Company.name)
            .all()
        )

    return render_template(
        "companies/list.html",
        companies=companies,
        search=search,
    )


# ==========================================================
# ADD COMPANY
# ==========================================================
@company.route(
    "/companies/add",
    methods=["GET", "POST"]
)
def add_company():

    if request.method == "POST":

        name = request.form["name"].strip()

        existing_company = Company.query.filter(
            Company.name.ilike(name)
        ).first()

        if existing_company:

            flash(
                "Company already exists.",
                "warning",
            )

            return redirect(request.url)

        new_company = Company(
            name=name,
        )

        db.session.add(new_company)
        db.session.commit()

        flash(
            "Company added successfully!",
            "success",
        )

        return redirect(
            url_for("company.company_list")
        )

    return render_template(
        "companies/add.html",
    )


# ==========================================================
# EDIT COMPANY
# ==========================================================
@company.route(
    "/companies/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_company(id):

    company_data = Company.query.get_or_404(id)

    if request.method == "POST":

        company_data.name = request.form["name"].strip()

        db.session.commit()

        flash(
            "Company updated successfully!",
            "warning",
        )

        return redirect(
            url_for("company.company_list")
        )

    return render_template(
        "companies/edit.html",
        company=company_data,
    )


# ==========================================================
# DELETE COMPANY
# ==========================================================
@company.route("/companies/delete/<int:id>")
def delete_company(id):

    company_data = Company.query.get_or_404(id)

    db.session.delete(company_data)
    db.session.commit()

    flash(
        "Company deleted successfully!",
        "danger",
    )

    return redirect(
        url_for("company.company_list")
    )