from flask import Blueprint

status = Blueprint("status", __name__)


@status.get("/healthz")
def healthz():
    return {"status": "ok"}
