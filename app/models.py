
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="customer"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


class Room(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    room_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    room_type = db.Column(
        db.String(50),
        nullable=False
    )

    floor = db.Column(
        db.Integer,
        nullable=False
    )

    price_per_night = db.Column(
        db.Float,
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False,
        default=2
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="available"
    )

    housekeeping_status = db.Column(
        db.String(30),
        nullable=False,
        default="clean"
    )

    description = db.Column(
        db.Text,
        nullable=True
    )


class Booking(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_reference = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("room.id"),
        nullable=False
    )

    check_in = db.Column(
        db.Date,
        nullable=False
    )

    check_out = db.Column(
        db.Date,
        nullable=False
    )

    guests = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    total_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="reservation"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "bookings",
            lazy=True
        )
    )

    room = db.relationship(
        "Room",
        backref=db.backref(
            "bookings",
            lazy=True
        )
    )


class Invoice(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("booking.id"),
        nullable=False
    )

    subtotal = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    tax_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    discount_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    paid_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    balance_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="unpaid"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    booking = db.relationship(
        "Booking",
        backref=db.backref(
            "invoice",
            uselist=False
        )
    )

    items = db.relationship(
        "InvoiceItem",
        backref="invoice",
        lazy=True,
        cascade="all, delete-orphan"
    )

    payments = db.relationship(
        "Payment",
        backref="invoice",
        lazy=True
    )


class InvoiceItem(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey("invoice.id"),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False,
        default=1
    )

    unit_price = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    total_price = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    item_type = db.Column(
        db.String(30),
        nullable=False,
        default="room"
    )


class Payment(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    payment_reference = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey("invoice.id"),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    payment_method = db.Column(
        db.String(30),
        nullable=False,
        default="cash"
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="completed"
    )

    transaction_reference = db.Column(
        db.String(100),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    payment_date = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    received_by_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    received_by = db.relationship(
        "User",
        foreign_keys=[received_by_id]
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )
