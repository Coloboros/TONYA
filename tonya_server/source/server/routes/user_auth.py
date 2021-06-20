import json

from flask import request
from flask import jsonify

from source.server.app import app
from source.settings import ROUTES_API_PREFIX
from source.db.database import DataBase

auth_url = f'/{ROUTES_API_PREFIX}/user/auth'

@app.route(f"{auth_url}/<tocken>", methods=["GET"])
def user_auth(tocken):
    db = DataBase()
    db.get_tocken(tocken)

    return jsonify(True)

@app.route(f"{auth_url}/<tocken>", methods=["POST"])
def user_auth_post(tocken):
    print(request.body)
    return jsonify(True)

@app.route(f"{auth_url}/", methods=["POST"])
def user_auth_add_tocken():
    db = DataBase()
    json_body = request.get_data().decode("utf-8")
    body = json.loads(json_body)
    user_id = body["user_id"]
    bot_type = body["bot_type"]

    # db.add_bot(str(user_id), str(bot_type))
    user = db.add_user(str(user_id), str(bot_type))
    if user != None:
        tocken = db.generate_tocken(user).value
        return jsonify(tocken)

    return jsonify(None)
