from source.server.app import app
from source.settings import ROUTES_API_PREFIX
from flask import jsonify

import random as rnd
def rand_numbers(count):
    return [rnd.randint(50, 150) for i in range(count)]

@app.route("/")
def index():
    return "Hello"

@app.route(f"/{ROUTES_API_PREFIX}/user/pressue/test", methods=["GET"])
def user_pressue_fixed():
    return jsonify(
        [150, 140, 130, 80, 110, 130, 150, 140, 130, 80, 110, 130]
    )

@app.route(f"/{ROUTES_API_PREFIX}/user/pressue/<int:year>/<int:month>/<int:day>", methods=["GET"])
def user_pressue_day(year, month, day):
    return jsonify(rand_numbers(12))

@app.route(f"/{ROUTES_API_PREFIX}/user/pressue/<int:year>/<int:month>", methods=["GET"])
def user_pressue_month(year, month):
    return jsonify(rand_numbers(12))

@app.route(f"/{ROUTES_API_PREFIX}/user/pressue/<int:year>", methods=["GET"])
def user_pressue_year(year):
    return jsonify(rand_numbers(12))
