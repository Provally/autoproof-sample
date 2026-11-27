import os

from flask import Flask

from app import db
from app.auth import auth, load_user
from app.files import files
from app.invoices import invoices
from app.reports import reports
from app.status import status

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
db.init_app(app)


@app.before_request
def before_request():
    load_user()


app.register_blueprint(auth)
app.register_blueprint(invoices)
app.register_blueprint(reports)
app.register_blueprint(files)
app.register_blueprint(status)
