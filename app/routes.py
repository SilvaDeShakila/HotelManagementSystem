from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from datetime import datetime
import random
import string

from . import db
from .models import Room, Booking, User, Invoice, InvoiceItem, Payment


main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():

    total_rooms = Room.query.count()

    available_rooms = Room.query.filter_by(
        status="available"
    ).count()

    occupied_rooms = Room.query.filter_by(
        status="occupied"
    ).count()

    cleaning_rooms = Room.query.filter_by(
        status="cleaning"
    ).count()

    maintenance_rooms = Room.query.filter_by(
        status="maintenance"
    ).count()

    total_bookings = Booking.query.count()

    active_bookings = Booking.query.filter(
        Booking.status.notin_(["cancelled", "checked-out"])
    ).count()

    total_customers = User.query.filter_by(
        role="customer"
    ).count()

    total_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Booking.total_amount),
            0
        )
    ).filter(
        Booking.status != "cancelled"
    ).scalar()

    recent_bookings = Booking.query.order_by(
        Booking.id.desc()
    ).limit(5).all()

    if total_rooms > 0:
        occupancy_rate = round(
            (occupied_rooms / total_rooms) * 100,
            1
        )
    else:
        occupancy_rate = 0

    return render_template(
        "dashboard.html",
        total_rooms=total_rooms,
        available_rooms=available_rooms,
        occupied_rooms=occupied_rooms,
        cleaning_rooms=cleaning_rooms,
        maintenance_rooms=maintenance_rooms,
        total_bookings=total_bookings,
        active_bookings=active_bookings,
        total_customers=total_customers,
        total_revenue=total_revenue,
        occupancy_rate=occupancy_rate,
        recent_bookings=recent_bookings
    )


@main.route("/guests")
@login_required
def guests():

    guests = User.query.filter_by(
        role="customer"
    ).order_by(
        User.name.asc()
    ).all()

    return render_template(
        "guests.html",
        guests=guests
    )


@main.route("/rooms")
@login_required
def rooms():
    all_rooms = Room.query.order_by(Room.room_number.asc()).all()

    return render_template(
        "rooms.html",
        rooms=all_rooms
    )


@main.route("/rooms/add", methods=["GET", "POST"])
@login_required
def add_room():

    if request.method == "POST":

        room_number = request.form.get("room_number", "").strip()
        room_type = request.form.get("room_type", "").strip()
        floor = request.form.get("floor", "").strip()
        price = request.form.get("price_per_night", "").strip()
        capacity = request.form.get("capacity", "").strip()
        status = request.form.get("status", "available").strip()
        description = request.form.get("description", "").strip()

        if not room_number or not room_type or not floor or not price:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("main.add_room"))

        existing_room = Room.query.filter_by(
            room_number=room_number
        ).first()

        if existing_room:
            flash("Room number already exists.", "warning")
            return redirect(url_for("main.add_room"))

        room = Room(
            room_number=room_number,
            room_type=room_type,
            floor=int(floor),
            price_per_night=float(price),
            capacity=int(capacity or 2),
            status=status,
            description=description
        )

        db.session.add(room)
        db.session.commit()

        flash("Room added successfully.", "success")

        return redirect(url_for("main.rooms"))

    return render_template("add_room.html")


@main.route("/rooms/edit/<int:room_id>", methods=["GET", "POST"])
@login_required
def edit_room(room_id):

    room = db.session.get(Room, room_id)

    if not room:
        flash("Room not found.", "danger")
        return redirect(url_for("main.rooms"))

    if request.method == "POST":

        room_number = request.form.get("room_number", "").strip()
        room_type = request.form.get("room_type", "").strip()
        floor = request.form.get("floor", "").strip()
        price = request.form.get("price_per_night", "").strip()
        capacity = request.form.get("capacity", "").strip()
        status = request.form.get("status", "available").strip()
        description = request.form.get("description", "").strip()

        if not room_number or not room_type or not floor or not price:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("main.edit_room", room_id=room.id))

        existing_room = Room.query.filter(
            Room.room_number == room_number,
            Room.id != room.id
        ).first()

        if existing_room:
            flash("Another room already uses this room number.", "warning")
            return redirect(url_for("main.edit_room", room_id=room.id))

        room.room_number = room_number
        room.room_type = room_type
        room.floor = int(floor)
        room.price_per_night = float(price)
        room.capacity = int(capacity or 2)
        room.status = status
        room.description = description

        db.session.commit()

        flash("Room updated successfully.", "success")

        return redirect(url_for("main.rooms"))

    return render_template(
        "edit_room.html",
        room=room
    )


@main.route("/rooms/delete/<int:room_id>", methods=["POST"])
@login_required
def delete_room(room_id):

    room = db.session.get(Room, room_id)

    if not room:
        flash("Room not found.", "danger")
        return redirect(url_for("main.rooms"))

    db.session.delete(room)
    db.session.commit()

    flash("Room deleted successfully.", "success")

    return redirect(url_for("main.rooms"))


@main.route("/bookings")
@login_required
def bookings():

    all_bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "bookings.html",
        bookings=all_bookings
    )


@main.route("/bookings/add", methods=["GET", "POST"])
@login_required
def add_booking():

    users = User.query.order_by(User.name.asc()).all()
    rooms = Room.query.order_by(Room.room_number.asc()).all()

    if request.method == "POST":

        user_id = request.form.get("user_id", "").strip()
        room_id = request.form.get("room_id", "").strip()
        check_in_text = request.form.get("check_in", "").strip()
        check_out_text = request.form.get("check_out", "").strip()
        guests_text = request.form.get("guests", "1").strip()
        notes = request.form.get("notes", "").strip()

        if not user_id or not room_id or not check_in_text or not check_out_text:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("main.add_booking"))

        try:
            check_in = datetime.strptime(check_in_text, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_text, "%Y-%m-%d").date()
            guests = int(guests_text)
        except ValueError:
            flash("Invalid booking information.", "danger")
            return redirect(url_for("main.add_booking"))

        if check_out <= check_in:
            flash("Check-out date must be after check-in date.", "warning")
            return redirect(url_for("main.add_booking"))

        if guests < 1:
            flash("Number of guests must be at least 1.", "warning")
            return redirect(url_for("main.add_booking"))

        user = db.session.get(User, int(user_id))
        room = db.session.get(Room, int(room_id))

        if not user:
            flash("Selected guest was not found.", "danger")
            return redirect(url_for("main.add_booking"))

        if not room:
            flash("Selected room was not found.", "danger")
            return redirect(url_for("main.add_booking"))

        if room.status != "available":
            flash("This room is not currently available.", "warning")
            return redirect(url_for("main.add_booking"))

        if guests > room.capacity:
            flash(
                f"This room can accommodate maximum {room.capacity} guests.",
                "warning"
            )
            return redirect(url_for("main.add_booking"))

        overlapping_booking = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.status.notin_(["cancelled", "checked-out"]),
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()

        if overlapping_booking:
            flash(
                "This room is already booked for the selected dates.",
                "danger"
            )
            return redirect(url_for("main.add_booking"))

        nights = (check_out - check_in).days
        total_amount = nights * room.price_per_night

        booking_reference = (
            "HTL-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=5
                )
            )
        )

        booking = Booking(
            booking_reference=booking_reference,
            user_id=user.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_amount=total_amount,
            status="reservation",
            notes=notes
        )

        db.session.add(booking)
        db.session.commit()

        flash(
            f"Booking {booking_reference} created successfully.",
            "success"
        )

        return redirect(url_for("main.bookings"))

    return render_template(
        "add_booking.html",
        users=users,
        rooms=rooms
    )


@main.route("/bookings/edit/<int:booking_id>", methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("main.bookings"))

    users = User.query.order_by(User.name.asc()).all()
    rooms = Room.query.order_by(Room.room_number.asc()).all()

    if request.method == "POST":

        user_id = request.form.get("user_id", "").strip()
        room_id = request.form.get("room_id", "").strip()
        check_in_text = request.form.get("check_in", "").strip()
        check_out_text = request.form.get("check_out", "").strip()
        guests_text = request.form.get("guests", "1").strip()
        status = request.form.get("status", "reservation").strip()
        notes = request.form.get("notes", "").strip()

        try:
            check_in = datetime.strptime(check_in_text, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_text, "%Y-%m-%d").date()
            guests = int(guests_text)
        except ValueError:
            flash("Invalid booking information.", "danger")
            return redirect(url_for("main.edit_booking", booking_id=booking.id))

        user = db.session.get(User, int(user_id))
        room = db.session.get(Room, int(room_id))

        if not user or not room:
            flash("Selected guest or room was not found.", "danger")
            return redirect(url_for("main.edit_booking", booking_id=booking.id))

        if check_out <= check_in:
            flash("Check-out date must be after check-in date.", "warning")
            return redirect(url_for("main.edit_booking", booking_id=booking.id))

        if guests < 1 or guests > room.capacity:
            flash("Invalid number of guests for this room.", "warning")
            return redirect(url_for("main.edit_booking", booking_id=booking.id))

        overlapping_booking = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.id != booking.id,
            Booking.status.notin_(["cancelled", "checked-out"]),
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()

        if overlapping_booking:
            flash(
                "This room is already booked for the selected dates.",
                "danger"
            )
            return redirect(url_for("main.edit_booking", booking_id=booking.id))

        nights = (check_out - check_in).days

        booking.user_id = user.id
        booking.room_id = room.id
        booking.check_in = check_in
        booking.check_out = check_out
        booking.guests = guests
        booking.total_amount = nights * room.price_per_night
        booking.status = status
        booking.notes = notes

        db.session.commit()

        flash("Booking updated successfully.", "success")

        return redirect(url_for("main.bookings"))

    return render_template(
        "edit_booking.html",
        booking=booking,
        users=users,
        rooms=rooms
    )


@main.route("/bookings/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("main.bookings"))

    if booking.status in ["checked-out", "cancelled"]:
        flash("This booking cannot be cancelled.", "warning")
        return redirect(url_for("main.bookings"))

    booking.status = "cancelled"

    db.session.commit()

    flash(
        f"Booking {booking.booking_reference} cancelled successfully.",
        "success"
    )

    return redirect(url_for("main.bookings"))


@main.route("/bookings/check-in/<int:booking_id>", methods=["POST"])
@login_required
def check_in_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("main.bookings"))

    if booking.status != "confirmed":
        flash(
            "Only confirmed bookings can be checked in.",
            "warning"
        )
        return redirect(url_for("main.bookings"))

    if booking.room.status not in ["available", "occupied"]:
        flash(
            "The room is not ready for check-in.",
            "warning"
        )
        return redirect(url_for("main.bookings"))

    booking.status = "checked-in"
    booking.room.status = "occupied"

    db.session.commit()

    flash(
        f"Guest checked in successfully. Room {booking.room.room_number} is now occupied.",
        "success"
    )

    return redirect(url_for("main.bookings"))


@main.route("/bookings/check-out/<int:booking_id>", methods=["POST"])
@login_required
def check_out_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("main.bookings"))

    if booking.status != "checked-in":
        flash(
            "Only checked-in bookings can be checked out.",
            "warning"
        )
        return redirect(url_for("main.bookings"))

    booking.status = "checked-out"
    booking.room.status = "cleaning"

    db.session.commit()

    flash(
        f"Guest checked out successfully. Room {booking.room.room_number} is now marked for cleaning.",
        "success"
    )

    return redirect(url_for("main.bookings"))


@main.route("/housekeeping")
@login_required
def housekeeping():

    all_rooms = Room.query.order_by(
        Room.floor.asc(),
        Room.room_number.asc()
    ).all()

    return render_template(
        "housekeeping.html",
        rooms=all_rooms
    )


@main.route("/housekeeping/update/<int:room_id>", methods=["POST"])
@login_required
def update_housekeeping(room_id):

    room = db.session.get(Room, room_id)

    if not room:
        flash("Room not found.", "danger")
        return redirect(url_for("main.housekeeping"))

    housekeeping_status = request.form.get(
        "housekeeping_status",
        "clean"
    ).strip()

    allowed_statuses = [
        "dirty",
        "cleaning",
        "clean",
        "inspected",
        "maintenance"
    ]

    if housekeeping_status not in allowed_statuses:
        flash("Invalid housekeeping status.", "danger")
        return redirect(url_for("main.housekeeping"))

    room.housekeeping_status = housekeeping_status

    if housekeeping_status == "maintenance":
        room.status = "maintenance"

    elif housekeeping_status in ["dirty", "cleaning"]:
        room.status = "cleaning"

    elif housekeeping_status in ["clean", "inspected"]:
        if room.status != "occupied":
            room.status = "available"

    db.session.commit()

    flash(
        f"Room {room.room_number} housekeeping status updated.",
        "success"
    )

    return redirect(url_for("main.housekeeping"))




def generate_invoice_number():
    while True:
        number = (
            "INV-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=5
                )
            )
        )

        if not Invoice.query.filter_by(
            invoice_number=number
        ).first():
            return number


def generate_payment_reference():
    while True:
        reference = (
            "PAY-"
            + datetime.now().strftime("%Y%m%d")
            + "-"
            + "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=5
                )
            )
        )

        if not Payment.query.filter_by(
            payment_reference=reference
        ).first():
            return reference


def update_invoice_balance(invoice):
    paid = db.session.query(
        db.func.coalesce(
            db.func.sum(Payment.amount),
            0
        )
    ).filter(
        Payment.invoice_id == invoice.id,
        Payment.status == "completed"
    ).scalar()

    invoice.paid_amount = round(float(paid or 0), 2)

    invoice.balance_amount = round(
        max(
            float(invoice.total_amount or 0)
            - invoice.paid_amount,
            0
        ),
        2
    )

    if invoice.paid_amount <= 0:
        invoice.status = "unpaid"

    elif invoice.paid_amount < invoice.total_amount:
        invoice.status = "partial"

    else:
        invoice.status = "paid"


@main.route("/payments")
@login_required
def payments():

    total_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Payment.amount),
            0
        )
    ).filter(
        Payment.status == "completed"
    ).scalar()

    today = datetime.now().date()

    today_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Payment.amount),
            0
        )
    ).filter(
        Payment.status == "completed",
        db.func.date(Payment.payment_date) == today
    ).scalar()

    pending_payments = db.session.query(
        db.func.coalesce(
            db.func.sum(Invoice.balance_amount),
            0
        )
    ).filter(
        Invoice.balance_amount > 0
    ).scalar()

    paid_amount = total_revenue or 0

    refund_amount = db.session.query(
        db.func.coalesce(
            db.func.sum(Payment.amount),
            0
        )
    ).filter(
        Payment.status == "refunded"
    ).scalar()

    outstanding_balance = pending_payments or 0

    recent_payments = Payment.query.order_by(
        Payment.id.desc()
    ).limit(10).all()

    invoices = Invoice.query.order_by(
        Invoice.id.desc()
    ).limit(10).all()

    return render_template(
        "payments.html",
        total_revenue=total_revenue,
        today_revenue=today_revenue,
        pending_payments=pending_payments,
        paid_amount=paid_amount,
        refund_amount=refund_amount,
        outstanding_balance=outstanding_balance,
        recent_payments=recent_payments,
        invoices=invoices
    )


@main.route("/payments/add", methods=["GET", "POST"])
@login_required
def add_payment():

    invoices = Invoice.query.order_by(
        Invoice.id.desc()
    ).all()

    if request.method == "POST":

        invoice_id = request.form.get("invoice_id", "").strip()
        amount_text = request.form.get("amount", "").strip()
        payment_method = request.form.get(
            "payment_method",
            "cash"
        ).strip()
        transaction_reference = request.form.get(
            "transaction_reference",
            ""
        ).strip()
        notes = request.form.get(
            "notes",
            ""
        ).strip()

        if not invoice_id or not amount_text:
            flash(
                "Invoice and payment amount are required.",
                "danger"
            )
            return redirect(url_for("main.add_payment"))

        invoice = db.session.get(
            Invoice,
            int(invoice_id)
        )

        if not invoice:
            flash(
                "Invoice not found.",
                "danger"
            )
            return redirect(url_for("main.add_payment"))

        try:
            amount = float(amount_text)
        except ValueError:
            flash(
                "Invalid payment amount.",
                "danger"
            )
            return redirect(url_for("main.add_payment"))

        if amount <= 0:
            flash(
                "Payment amount must be greater than zero.",
                "danger"
            )
            return redirect(url_for("main.add_payment"))

        update_invoice_balance(invoice)

        if amount > invoice.balance_amount:
            flash(
                f"Payment cannot exceed outstanding balance of "
                f"₨ {invoice.balance_amount:,.2f}.",
                "danger"
            )
            return redirect(url_for("main.add_payment"))

        payment = Payment(
            payment_reference=generate_payment_reference(),
            invoice_id=invoice.id,
            amount=round(amount, 2),
            payment_method=payment_method,
            status="completed",
            transaction_reference=(
                transaction_reference
                if transaction_reference
                else None
            ),
            notes=notes if notes else None,
            received_by_id=current_user.id
        )

        db.session.add(payment)
        db.session.flush()

        update_invoice_balance(invoice)

        db.session.commit()

        flash(
            f"Payment {payment.payment_reference} recorded successfully.",
            "success"
        )

        return redirect(
            url_for(
                "main.payment_details",
                payment_id=payment.id
            )
        )

    return render_template(
        "add_payment.html",
        invoices=invoices
    )


@main.route("/payments/<int:payment_id>")
@login_required
def payment_details(payment_id):

    payment = db.session.get(
        Payment,
        payment_id
    )

    if not payment:
        flash(
            "Payment not found.",
            "danger"
        )
        return redirect(url_for("main.payments"))

    return render_template(
        "payment_details.html",
        payment=payment
    )


@main.route("/invoices")
@login_required
def invoices():

    invoices = Invoice.query.order_by(
        Invoice.id.desc()
    ).all()

    return render_template(
        "invoices.html",
        invoices=invoices
    )


@main.route("/invoices/<int:invoice_id>")
@login_required
def invoice_details(invoice_id):

    invoice = db.session.get(
        Invoice,
        invoice_id
    )

    if not invoice:
        flash(
            "Invoice not found.",
            "danger"
        )
        return redirect(url_for("main.invoices"))

    update_invoice_balance(invoice)
    db.session.commit()

    return render_template(
        "invoice_details.html",
        invoice=invoice
    )


@main.route("/invoices/create/<int:booking_id>", methods=["GET", "POST"])
@login_required
def create_invoice(booking_id):

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:
        flash(
            "Booking not found.",
            "danger"
        )
        return redirect(url_for("main.bookings"))

    existing = Invoice.query.filter_by(
        booking_id=booking.id
    ).first()

    if existing:
        flash(
            "An invoice already exists for this booking.",
            "info"
        )
        return redirect(
            url_for(
                "main.invoice_details",
                invoice_id=existing.id
            )
        )

    subtotal = float(
        booking.total_amount or 0
    )

    tax_amount = 0
    discount_amount = 0

    total_amount = round(
        subtotal + tax_amount - discount_amount,
        2
    )

    invoice = Invoice(
        invoice_number=generate_invoice_number(),
        booking_id=booking.id,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
        paid_amount=0,
        balance_amount=total_amount,
        status="unpaid"
    )

    db.session.add(invoice)
    db.session.flush()

    item = InvoiceItem(
        invoice_id=invoice.id,
        description=(
            f"Room {booking.room.room_number} "
            f"({booking.check_in} to {booking.check_out})"
        ),
        quantity=1,
        unit_price=subtotal,
        total_price=subtotal,
        item_type="room"
    )

    db.session.add(item)

    db.session.commit()

    flash(
        f"Invoice {invoice.invoice_number} created successfully.",
        "success"
    )

    return redirect(
        url_for(
            "main.invoice_details",
            invoice_id=invoice.id
        )
    )


@main.route("/payments/<int:payment_id>/refund", methods=["POST"])
@login_required
def refund_payment(payment_id):

    payment = db.session.get(
        Payment,
        payment_id
    )

    if not payment:
        flash(
            "Payment not found.",
            "danger"
        )
        return redirect(url_for("main.payments"))

    if payment.status != "completed":
        flash(
            "Only completed payments can be refunded.",
            "warning"
        )
        return redirect(
            url_for(
                "main.payment_details",
                payment_id=payment.id
            )
        )

    payment.status = "refunded"

    invoice = payment.invoice

    db.session.flush()
    update_invoice_balance(invoice)

    db.session.commit()

    flash(
        f"Payment {payment.payment_reference} refunded.",
        "success"
    )

    return redirect(
        url_for(
            "main.payment_details",
            payment_id=payment.id
        )
    )
