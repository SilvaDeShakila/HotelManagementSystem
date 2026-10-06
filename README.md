# 🏨 Hotel Management System

A modern, premium, and extensible **Hotel Management System (HMS)** built with **Python, Flask, SQLAlchemy, Flask-Login, Flask-WTF, and Bootstrap**.

The system is being developed as a complete hotel operations platform covering reservations, guests, rooms, housekeeping, payments, invoices, staff roles, reporting, analytics, and administrative operations.

> **Project Status:** Active Development 🚧
> The current release contains the core hotel management foundation, reservation workflow, housekeeping, payment processing, invoices, and a premium responsive interface. Advanced modules are being developed progressively.

---

## ✨ Project Vision

The goal of this project is to build a professional hotel management platform that can support the daily operations of a modern hotel from a single system.

The system is designed around:

* 🏨 Hotel operations
* 🛏️ Room management
* 📅 Reservations
* 👤 Guest management
* 🧹 Housekeeping
* 💳 Payments
* 🧾 Invoices
* 📊 Business analytics
* 🔐 Role-based security
* 🔔 Notifications
* ⭐ Guest reviews
* 📈 Management reports
* ⚙️ Configurable hotel settings

The architecture is intentionally modular so additional hotel features can be introduced without rebuilding the application from scratch.

---

# 🚀 Current Features

## 🔐 Authentication

* Customer registration
* Customer login
* Logout
* Password hashing
* Session-based authentication
* Flask-Login integration
* Protected application routes

---

## 🏨 Dashboard

The dashboard provides a centralized overview of hotel operations.

Current dashboard capabilities include:

* Total rooms
* Available rooms
* Occupied rooms
* Cleaning rooms
* Maintenance rooms
* Total bookings
* Active bookings
* Total customers
* Revenue overview
* Occupancy overview
* Recent bookings

The dashboard will continue to evolve into a full hotel management command center.

---

# 🛏️ Room Management

Room management currently supports:

* Room numbers
* Room types
* Floor numbers
* Room pricing
* Guest capacity
* Room descriptions
* Room operational status
* Housekeeping status
* Add room
* Edit room
* Room listing

### Room Status

The system supports operational room states such as:

* Available
* Occupied
* Cleaning
* Maintenance

---

# 📅 Reservation & Booking Management

The reservation system supports:

* Creating bookings
* Editing bookings
* Booking references
* Guest selection
* Room selection
* Check-in date
* Check-out date
* Guest count
* Booking notes
* Automatic stay amount calculation
* Booking status management
* Booking cancellation
* Double-booking prevention
* Check-in workflow
* Check-out workflow

### Booking Lifecycle

```text
Available
    ↓
Reservation
    ↓
Confirmed
    ↓
Checked-in
    ↓
Checked-out
```

Cancelled reservations are handled separately.

---

# 🧹 Housekeeping Management

Housekeeping functionality allows hotel staff to manage room cleaning and inspection states.

Supported housekeeping states include:

* Dirty
* Cleaning
* Clean
* Inspected
* Maintenance

The housekeeping status is connected to the room's operational status where appropriate.

Example workflow:

```text
Checked-out
     ↓
Dirty / Cleaning
     ↓
Clean
     ↓
Inspected
     ↓
Available
```

---

# 💳 Payment Management

The financial module currently supports:

* Payment records
* Payment references
* Invoice-based payments
* Partial payments
* Multiple payments
* Payment methods
* Transaction references
* Payment notes
* Payment status
* Received-by tracking
* Outstanding balance calculation
* Automatic invoice balance updates
* Payment history
* Refund workflow

### Supported Payment Methods

* Cash
* Card
* Bank Transfer
* Online Payment
* Other

### Payment Lifecycle

```text
Unpaid
   ↓
Partial
   ↓
Paid
```

---

# 🧾 Invoice Management

Invoice functionality currently supports:

* Automatic invoice numbers
* Booking-linked invoices
* Invoice items
* Room charges
* Subtotal
* Tax amount
* Discount amount
* Total amount
* Paid amount
* Outstanding balance
* Invoice status
* Payment history
* Invoice details
* Invoice creation from bookings

### Invoice Status

```text
Unpaid
Partial
Paid
```

The invoice system is designed to support future hotel charges such as:

* Extra beds
* Food & beverage
* Laundry
* Transport
* Room service
* Minibar
* Spa
* Other hotel services

---

# 👥 Guest Management

The guest management foundation includes:

* Customer accounts
* Guest-linked bookings
* Guest booking history
* Customer authentication

Future guest-profile expansion will include:

* Contact information
* Identification details
* Guest preferences
* Stay history
* Special requests
* VIP status
* Guest notes

---

# 👨‍💼 Staff & Role Management

A complete role-based access control system is planned for hotel staff.

Planned roles include:

| Role         | Responsibility                     |
| ------------ | ---------------------------------- |
| Admin        | Full system control                |
| Manager      | Hotel operations and reports       |
| Receptionist | Reservations and guest operations  |
| Housekeeping | Room cleaning and room status      |
| Accountant   | Payments, invoices and finance     |
| Customer     | Reservations and personal bookings |

Role permissions will be enforced at the backend level rather than relying only on frontend visibility.

---

# 📊 Analytics & Reporting

The analytics system is planned to provide hotel management with detailed business information.

Planned reports include:

* Revenue reports
* Daily revenue
* Monthly revenue
* Yearly revenue
* Occupancy reports
* Booking reports
* Cancellation reports
* Payment reports
* Outstanding balance reports
* Room performance
* Room-type performance
* Guest statistics
* Housekeeping reports
* Staff activity reports

Future dashboards will include interactive charts and date-range filtering.

---

# 💰 Advanced Pricing System

Planned pricing capabilities include:

* Seasonal pricing
* Weekend pricing
* Holiday pricing
* Room-type pricing
* Dynamic pricing
* Long-stay discounts
* Early booking discounts
* Promotional discounts
* Corporate rates
* Coupon codes
* Tax configuration
* Service charges

The pricing architecture will be designed to calculate the final booking amount automatically.

---

# 🛎️ Hotel Services

Future hotel services will support additional billable services such as:

* Restaurant
* Room service
* Laundry
* Minibar
* Airport transfer
* Extra bed
* Spa
* Activities
* Other hotel services

These services will be capable of being attached to an invoice.

---

# 🔔 Notifications

Planned notification functionality includes:

* Booking confirmation
* Booking cancellation
* Payment confirmation
* Invoice notification
* Check-in reminder
* Check-out reminder
* Outstanding payment reminder
* Housekeeping notifications
* Administrative notifications

Email and in-system notifications will be supported progressively.

---

# ⭐ Reviews & Ratings

A future guest review module will support:

* Hotel ratings
* Room ratings
* Guest reviews
* Review moderation
* Review status
* Rating analytics

Only eligible guests will be allowed to submit verified stay reviews.

---

# 🔐 Security

Security is a major part of the project's development roadmap.

Planned and implemented security mechanisms include:

* Password hashing
* Session authentication
* Login protection
* Role-based access control
* CSRF protection
* Secure form validation
* Authorization checks
* Input validation
* Database constraints
* Secure configuration
* Environment variables
* Audit logging
* Secure error handling

Sensitive information such as:

```text
.env
database files
virtual environments
API keys
passwords
secret keys
```

must never be committed to the public repository.

---

# 📝 Audit Logging

A future audit system will record important administrative actions.

Examples:

```text
User logged in
Booking created
Booking modified
Booking cancelled
Payment recorded
Payment refunded
Invoice created
Room status changed
User role changed
```

Audit logs will help hotel management track operational activity.

---

# 🗄️ Database

The current development environment uses **SQLite**.

The architecture is designed to support production database systems such as:

* MySQL
* PostgreSQL

SQLAlchemy is used as the ORM layer.

### Current Core Models

```text
User
Room
Booking
Invoice
InvoiceItem
Payment
```

Additional models will be introduced as advanced modules are implemented.

---

# 🏗️ Technology Stack

## Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* Flask-Login
* Flask-WTF
* Werkzeug
* python-dotenv

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Custom Premium CSS
* Responsive UI

## Database

Development:

```text
SQLite
```

Production target:

```text
MySQL / PostgreSQL
```

## Deployment

Planned deployment environments include:

* Microsoft Azure
* Linux server
* Windows server
* Gunicorn-based deployment

---

# 🎨 Premium UI

The application uses a custom premium visual design system.

UI goals include:

* Modern hotel-management dashboard
* Premium dark sidebar
* Glass-style navigation
* Gold accent system
* Responsive layouts
* Smooth transitions
* Interactive cards
* Professional tables
* Status badges
* Responsive forms
* Mobile-friendly layouts
* Consistent financial interfaces

The design system is implemented primarily through:

```text
app/static/css/premium.css
```

---

# 📁 Project Structure

```text
HotelManagementSystem/
│
├── app.py
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   │
│   └── static/
│       ├── css/
│       │   └── premium.css
│       └── js/
│
├── templates/
│   ├── dashboard.html
│   ├── rooms.html
│   ├── add_room.html
│   ├── edit_room.html
│   ├── bookings.html
│   ├── add_booking.html
│   ├── edit_booking.html
│   ├── housekeeping.html
│   ├── guests.html
│   ├── payments.html
│   ├── add_payment.html
│   ├── payment_details.html
│   ├── invoices.html
│   ├── invoice_details.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── bootstrap/
│   ├── images/
│   └── favicon.ico
│
├── instance/
│   └── hotel.db
│
├── requirements.txt
├── README.md
└── .gitignore
```

> `instance/` and other environment-specific files are intentionally excluded from the public Git repository.

---

# ⚙️ Local Development Setup

## 1. Clone the repository

```bash
git clone https://github.com/SilvaDeShakila/HotelManagementSystem.git
```

```bash
cd HotelManagementSystem
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

---

# 🔧 Environment Configuration

Production configuration should be stored in environment variables.

Example:

```env
SECRET_KEY=your-secure-secret-key
DATABASE_URL=your-production-database-url
```

Never commit real credentials or production secrets to GitHub.

---

# 🧪 Testing Roadmap

The project will progressively introduce automated testing.

Planned test coverage:

* Authentication
* Registration
* Login
* Authorization
* Room creation
* Room updates
* Booking creation
* Double-booking prevention
* Booking cancellation
* Check-in
* Check-out
* Housekeeping transitions
* Invoice creation
* Payment creation
* Partial payments
* Full payments
* Refunds
* Role permissions
* Security validation

---

# 🔄 Development Workflow

The project follows a Git-based development workflow.

Typical workflow:

```bash
git pull
```

Make changes, then:

```bash
git add .
git commit -m "Describe the change"
git push
```

The `main` branch represents the current stable project state.

---

# 🛣️ Development Roadmap

## Phase 1 — Core Foundation ✅

* [x] Flask application
* [x] SQLAlchemy database
* [x] Authentication
* [x] Customer registration
* [x] Login/logout
* [x] Room management
* [x] Booking management
* [x] Booking references
* [x] Double-booking prevention
* [x] Check-in/check-out
* [x] Housekeeping
* [x] Guest management foundation
* [x] Payment module
* [x] Invoice module
* [x] Partial payments
* [x] Multiple payments
* [x] Payment balance calculation
* [x] Refund workflow
* [x] Premium UI foundation

---

## Phase 2 — Security & Staff Management 🚧

* [ ] Admin role system
* [ ] Manager role
* [ ] Receptionist role
* [ ] Housekeeping role
* [ ] Accountant role
* [ ] Permission middleware
* [ ] CSRF protection
* [ ] Security hardening
* [ ] Audit logs
* [ ] Secure configuration

---

## Phase 3 — Advanced Hotel Operations 🚧

* [ ] Room types
* [ ] Room facilities
* [ ] Room images
* [ ] Room gallery
* [ ] Advanced availability search
* [ ] Guest profiles
* [ ] Guest preferences
* [ ] Extra beds
* [ ] Hotel services
* [ ] Service charges
* [ ] Taxes
* [ ] Discounts
* [ ] Coupons

---

## Phase 4 — Finance 🚧

* [ ] Advanced invoice items
* [ ] Automatic tax calculation
* [ ] Discounts
* [ ] Deposits
* [ ] Refund management
* [ ] Payment gateway integration
* [ ] Financial reports
* [ ] Revenue analytics
* [ ] Accounting reports

---

## Phase 5 — Analytics 🚧

* [ ] Revenue dashboard
* [ ] Occupancy dashboard
* [ ] Booking analytics
* [ ] Cancellation analytics
* [ ] Room performance
* [ ] Guest analytics
* [ ] Date-range reports
* [ ] Export reports
* [ ] PDF reports
* [ ] Excel reports

---

## Phase 6 — Guest Experience 🚧

* [ ] Guest profile
* [ ] Booking history
* [ ] Notifications
* [ ] Email confirmations
* [ ] Booking reminders
* [ ] Reviews
* [ ] Ratings
* [ ] Guest preferences
* [ ] Loyalty features

---

## Phase 7 — Production & Deployment 🚧

* [ ] Flask-Migrate
* [ ] Production database
* [ ] Production configuration
* [ ] Gunicorn
* [ ] Azure deployment
* [ ] Production logging
* [ ] Error monitoring
* [ ] Backup system
* [ ] Database restore workflow
* [ ] CI/CD pipeline

---

# 💾 Database & Backup Policy

The local development database is stored inside:

```text
instance/hotel.db
```

The database is intentionally excluded from GitHub.

For backup purposes, database files should be stored separately from source control.

Recommended backup strategy:

```text
Source Code → GitHub
Database → Separate Backup
Secrets → Secure Environment
Production Data → Automated Backup
```

---

# 🌐 Production Architecture

The long-term architecture is intended to evolve toward:

```text
                    ┌──────────────────────┐
                    │      Web Browser     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Flask Application  │
                    │   Authentication     │
                    │   Business Logic     │
                    │   REST/AJAX Layer    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │   Booking  │   │  Finance   │   │ Housekeep. │
       │   Module   │   │   Module   │   │   Module   │
       └────────────┘   └────────────┘   └────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │      SQLAlchemy      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Production Database  │
                    │ MySQL / PostgreSQL   │
                    └──────────────────────┘
```

---

# 📌 Important Security Rules

Before production deployment:

1. Never commit `.env`.
2. Never commit database credentials.
3. Never commit API keys.
4. Never commit production passwords.
5. Never use development `SECRET_KEY` in production.
6. Enable CSRF protection.
7. Validate all user input.
8. Enforce backend authorization.
9. Use HTTPS.
10. Use a production database.
11. Configure proper database backups.
12. Use secure password policies.
13. Keep dependencies updated.
14. Do not expose internal error traces to users.

---

# 📜 License

This project currently does not define a production open-source license.

License and distribution terms can be added before public production release.

---

# 👨‍💻 Development

This project is actively being developed as a full-featured hotel management platform.

The implementation is intentionally incremental:

```text
Foundation
    ↓
Security
    ↓
Operations
    ↓
Finance
    ↓
Analytics
    ↓
Guest Experience
    ↓
Production Deployment
```

The objective is to evolve the application into a scalable, secure, maintainable, and premium hotel management solution.

---

## ⭐ Project

**HotelManagementSystem**

GitHub:

https://github.com/SilvaDeShakila/HotelManagementSystem

