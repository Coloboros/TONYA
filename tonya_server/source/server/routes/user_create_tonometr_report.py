#
from source.server.app import app
from source.settings import ROUTES_API_PREFIX
from flask import jsonify, request
import json

from source.db.database import DataBase

@app.route(f"/api/user/set-tonometr-report/", methods=["POST"])
def create_tonometr_report():
    db = DataBase()
    json_body = request.get_data().decode("utf-8")
    body = json.loads(json_body)

    user_id = body["user_id"]

    top_pressue, bot_pressue, pulse = body["vals"]
    tags = body["tags"]

    user = db.get_user(user_id)

    db.create_report(user, top_pressue, bot_pressue, pulse, tags)

    print(user.tonometr_reports)

    return jsonify(True)
