import subprocess

from flask import Blueprint, request

from app.auth import get_current_user
from app.db import DATA_DIR

reports = Blueprint("reports", __name__)


def archive():
    get_current_user()
    name = request.form.get("name", "invoices")
    subprocess.check_output("tar czf /tmp/" + name + ".tgz -C " + DATA_DIR + " .", shell=True)
    return {"archive": "/tmp/" + name + ".tgz"}


@reports.get("/reports/disk")
def disk_usage():
    get_current_user()
    return {"usage": subprocess.check_output("df -h /srv/ledgerly", shell=True, text=True)}


reports.add_url_rule("/reports/archive", view_func=archive, methods=["POST"])
