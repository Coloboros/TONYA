from asyncio.runners import run
import json

from flask import request, render_template, jsonify

from source.server.app import app
from source.db.database import DataBase

from jinja2 import Template

@app.route(f"/pacients/", methods=["GET"])
def get_pacients():
    db = DataBase()
    pacients = db.get_users()
    ctx = { 'pacients': pacients }
    return render_template('pacients_row.html', **ctx)


@app.route(f"/pacient/<int:user_id>", methods=["GET"])
def get_pacient(user_id):
    db = DataBase()
    pacient = db.get_user(user_id)
    if pacient == None:
        return "<h1>WTF<h1>"
    ctx = { 'pacient': pacient }
    return render_template('pacient.html', **ctx)



import asyncio
from threading import Thread

from aiogram import Bot
from source.settings import BOT_TOCKEN
bot = Bot(token=BOT_TOCKEN)



@app.route(f"/pacient/<int:user_id>", methods=["POST"])
def get_pacient_post(user_id):
    db = DataBase()
    pacient = db.get_user(user_id)

    asyncio.run(bot.send_message(user_id, "msg"))


    return jsonify(True)
