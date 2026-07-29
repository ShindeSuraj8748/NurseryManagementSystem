from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database import db
from app.models import (
    Customer,
    Booking,
    BookingItem,
    PlantBatch
)

from datetime import datetime

bookings = Blueprint(
    "bookings",
    __name__
)


@bookings.route("/bookings")
def booking_list():

    bookings = (
        Booking.query
        .order_by(Booking.id.desc())
        .all()
    )

    return render_template(
        "bookings/list.html",
        bookings=bookings
    )


@bookings.route("/bookings/add", methods=["GET", "POST"])
def add_booking():

    customers = Customer.query.order_by(Customer.name).all()

    batches = (
        PlantBatch.query
        .order_by(PlantBatch.id.desc())
        .all()
    )

    if request.method == "POST":

        booking = Booking(

            booking_no=f"BK{Booking.query.count()+1:05d}",

            customer_id=int(
                request.form["customer_id"]
            ),

            booking_date=datetime.strptime(
                request.form["booking_date"],
                "%Y-%m-%d"
            ),

            advance_amount=float(
                request.form["advance_amount"]
            ),

            remarks=request.form["remarks"]

        )

        db.session.add(booking)
        db.session.flush()

        batch = PlantBatch.query.get_or_404(
            int(request.form["batch_id"])
        )

        quantity = int(
            request.form["quantity"]
        )

        price = float(
            request.form["price"]
        )

        total = quantity * price

        item = BookingItem(

            booking_id=booking.id,

            batch_id=batch.id,

            quantity=quantity,

            price_per_plant=price,

            total_price=total

        )

        batch.reserved_plants += quantity

        db.session.add(item)

        booking.calculate_totals()

        db.session.commit()

        flash(
            "Booking created successfully.",
            "success"
        )

        return redirect(
            url_for("bookings.booking_list")
        )

    return render_template(
        "bookings/add.html",
        customers=customers,
        batches=batches
    )
    
@bookings.route("/bookings/<int:booking_id>")
def booking_details(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )

    return render_template(

        "bookings/details.html",

        booking=booking

    )
    
    
@bookings.route("/bookings/<int:booking_id>/deliver", methods=["GET", "POST"])
def deliver_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.status == "Completed":

        flash(
            "Booking already completed.",
            "warning"
        )

        return redirect(
            url_for(
                "bookings.booking_details",
                booking_id=booking.id
            )
        )

    if request.method == "POST":

        booking.complete()

        db.session.commit()

        flash(
            "Plants delivered successfully.",
            "success"
        )

        return redirect(
            url_for(
                "bookings.booking_details",
                booking_id=booking.id
            )
        )

    return render_template(
        "bookings/deliver.html",
        booking=booking
    )