import json

from flask import request, render_template, jsonify

from source.server.app import app
from source.db.database import DataBase

from jinja2 import Template

@app.route(f"/pacients/", methods=["GET"])
def get_pacients():
    db = DataBase()

    pacients = db.get_users()

    ctx = {
        'pacients': pacients
    }

    return render_template('pacients_row.html', **ctx)
