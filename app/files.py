import os

from flask import Blueprint, abort, request

from app.auth import get_current_user
from app.db import ATTACHMENTS_DIR

files = Blueprint("files", __name__)


@files.get("/attachments/download")
def download():
    get_current_user()
    name = request.args.get("name", "")
    with open(os.path.join(ATTACHMENTS_DIR, name), "rb") as handle:
        return handle.read()


@files.get("/attachments/preview")
def preview():
    get_current_user()
    name = request.args.get("name", "")
    root = os.path.realpath(ATTACHMENTS_DIR)
    path = os.path.realpath(os.path.join(root, name))
    if os.path.commonpath([root, path]) != root or not os.path.isfile(path):
        abort(404)
    with open(path, "rb") as handle:
        return handle.read(4096)
