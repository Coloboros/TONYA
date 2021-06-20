from source.server.app import app
from source.settings import ROUTES_API_PREFIX
from flask import jsonify, request
import json
from datetime import datetime

from source.db.database import DataBase

@app.route(f"/api/user/set-property/", methods=["POST"])
def set_property():
    db = DataBase()
    json_body = request.get_data().decode("utf-8")
    body = json.loads(json_body)

    user_id = body['user_id']
    birthday_dict = body['birthday']
    birthday_date = datetime(
        year = birthday_dict['year'],
        month = birthday_dict['month'],
        day = birthday_dict['day'],
    )
    height = body['height']
    width = body['width']

    print(user_id)


    user = db.get_user(user_id)
    print(user)
    db.set_property(user, birthday_date, height, width)

    return jsonify(True)
