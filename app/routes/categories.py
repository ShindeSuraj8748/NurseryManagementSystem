from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app.database import db
from app.models import Category

categories = Blueprint("categories", __name__)


@categories.route("/categories")
def category_list():

    categories = (
        Category.query
        .order_by(Category.name)
        .all()
    )

    return render_template(
        "categories/list.html",
        categories=categories
    )


@categories.route(
    "/categories/add",
    methods=["GET", "POST"]
)
def add_category():

    if request.method == "POST":

        name = request.form["name"].strip()

        if Category.query.filter_by(name=name).first():

            flash(
                "Category already exists.",
                "warning"
            )

            return redirect(request.url)

        category = Category(name=name)

        db.session.add(category)
        db.session.commit()

        flash(
            "Category added successfully.",
            "success"
        )

        return redirect(
            url_for("categories.category_list")
        )

    return render_template(
        "categories/add.html"
    )


@categories.route(
    "/categories/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_category(id):

    category = Category.query.get_or_404(id)

    if request.method == "POST":

        category.name = request.form["name"]

        db.session.commit()

        flash(
            "Category updated successfully.",
            "success"
        )

        return redirect(
            url_for("categories.category_list")
        )

    return render_template(
        "categories/edit.html",
        category=category
    )


@categories.route("/categories/delete/<int:id>")
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    flash(
        "Category deleted successfully.",
        "danger"
    )

    return redirect(
        url_for("categories.category_list")
    )