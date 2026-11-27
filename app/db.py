import os
import sqlite3

from flask import g

DATA_DIR = os.environ.get("LEDGERLY_DATA", "data")
DB_PATH = os.path.join(DATA_DIR, "ledgerly.db")
# Attachments ship with the code, outside the data directory the service writes.
ATTACHMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attachments")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    number TEXT NOT NULL,
    customer TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""

SAMPLE_USERS = [("billing@acme.example",), ("finance@globex.example",)]

SAMPLE_INVOICES = [
    ("billing@acme.example", "INV-1001", "Acme Corp", 120000, "2026-10-01"),
    ("billing@acme.example", "INV-1002", "Initech", 45000, "2026-10-14"),
    ("finance@globex.example", "INV-2001", "Globex", 990000, "2026-10-20"),
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if "db" not in g:
        g.db = connect()
    return g.db


def close_db(_error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app):
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = connect()
    try:
        conn.executescript(SCHEMA)
        if not conn.execute("SELECT id FROM invoices LIMIT 1").fetchall():
            conn.executemany("INSERT INTO users (email) VALUES (?)", SAMPLE_USERS)
            conn.executemany(
                "INSERT INTO invoices (owner, number, customer, total_cents, created_at) VALUES (?, ?, ?, ?, ?)",
                SAMPLE_INVOICES,
            )
            conn.commit()
    finally:
        conn.close()
    app.teardown_appcontext(close_db)
