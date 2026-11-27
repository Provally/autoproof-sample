from flask import Blueprint, render_template_string, request

from app.auth import get_current_user
from app.db import get_db

invoices = Blueprint("invoices", __name__)

SORT_COLUMNS = {
    "number": "number",
    "customer": "customer",
    "total": "total_cents",
    "date": "created_at",
}


@invoices.get("/invoices")
def list_invoices():
    user = get_current_user()
    sort = SORT_COLUMNS.get(request.args.get("sort", ""), "created_at")
    rows = get_db().execute(
        f"SELECT number, customer, total_cents, created_at FROM invoices WHERE owner = ? ORDER BY {sort}",
        (user["email"],),
    ).fetchall()
    return {"invoices": [dict(row) for row in rows]}


@invoices.get("/invoices/search")
def search_invoices():
    user = get_current_user()
    customer = request.args.get("customer", "")
    rows = get_db().execute(
        "SELECT number, customer, total_cents FROM invoices WHERE owner = '" + user["email"]
        + "' AND customer LIKE '%" + customer + "%'"
    ).fetchall()
    return {"invoices": [dict(row) for row in rows]}


def preview_reminder():
    """Show how a payment reminder the user wrote renders, with a sample invoice in place of a real one."""
    user = get_current_user()
    template = request.form.get("template", "")
    invoice = {"number": "INV-0000", "customer": "Sample customer", "total": "0.00", "contact": user["email"]}
    return render_template_string(template, invoice=invoice)


invoices.add_url_rule("/invoices/reminder-preview", view_func=preview_reminder, methods=["POST"])
