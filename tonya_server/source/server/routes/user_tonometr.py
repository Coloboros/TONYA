from source.server.app import app
from source.settings import ROUTES_API_PREFIX
from flask import jsonify, request
import json

from source.db.database import DataBase

@app.route(f"/api/user/set-tonometr/", methods=["POST"])
def set_tonometr():
    db = DataBase()
    json_body = request.get_data().decode("utf-8")
    body = json.loads(json_body)

    user_id = body["user_id"]
    tonometr = body["tonometr"]

    user = db.get_user(user_id)
    db.set_tonometr(user, tonometr)

    return jsonify(True)
