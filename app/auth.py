import sqlite3

from flask import Blueprint, abort, g, request, session

from app.db import get_db

auth = Blueprint("auth", __name__)


def load_user():
    g.user = None
    user_id = session.get("user_id")
    if user_id is None:
        return
    rows = get_db().execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchall()
    if rows:
        g.user = rows[0]


def get_current_user():
    if g.get("user") is None:
        abort(401)
    return g.user


def signup():
    """Anyone may open an account for an address nobody holds; the response signs it in with a session cookie."""
    email = request.form.get("email", "").strip().lower()
    if "@" not in email:
        abort(400)
    db = get_db()
    try:
        cursor = db.execute("INSERT INTO users (email) VALUES (?)", (email,))
        db.commit()
    except sqlite3.IntegrityError:
        abort(409)
    session.clear()
    session["user_id"] = cursor.lastrowid
    return {"email": email}, 201


auth.add_url_rule("/signup", view_func=signup, methods=["POST"])
