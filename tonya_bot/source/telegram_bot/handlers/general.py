from os import stat
from aiogram.types.base import String
import json
import requests
from hashlib import md5
from xml.etree import ElementTree

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text

from source.telegram_bot.bot import dp, db, bot

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings

from source.settings import SERVER_HOST_AUTH_URL, SERVER_HOST_PROTOCOL, SERVER_HOST

import requests

req_headers_json = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

class SelectTanomenr(StatesGroup):
    waiting_for_input = State()

async def send_welcome(message: types.Message):

    data = {
        "bot_type": "telegram",
        "user_id": str(message.from_user.id)
    }

    print(SERVER_HOST_PROTOCOL + "://" + SERVER_HOST_AUTH_URL)
    response = requests.post(
        SERVER_HOST_PROTOCOL + "://" + SERVER_HOST_AUTH_URL,
        data=json.dumps(data),
        headers=req_headers_json)

    await message.answer(strings.start_content, reply_markup=ReplyKeyboardRemove())
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2')
    await SelectTanomenr.next()

async def select_tanometr_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.choice_tanometr_cancle)
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2', reply_markup=kb)
    await SelectTanomenr.next()


url_set_tonometr = SERVER_HOST_PROTOCOL + "://" + SERVER_HOST + 'user/set-tonometr/'

async def select_tanometr_input(message: types.Message, state: FSMContext):

    data = {
        "bot_type": "telegram",
        "user_id": str(message.from_user.id),
        "tonometr": message.text
    }
    response = requests.post(
        url_set_tonometr,
        data=json.dumps(data),
        headers=req_headers_json)

    if response.status_code != 200:
        print(url_set_tonometr)
        print(response.status_code)
        print('****ERROR**** upps in general select_tanometr_input')

    await message.answer(strings.choice_tanometr_finish, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

async def select_tanometr_cancle(message: types.Message, state: FSMContext):
    await message.answer(strings.choice_tanometr_cancle, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

async def home_cmd(message: types.Message):
    await message.answer(strings.main_menu, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(home_cmd, commands=['home'], state=default_state)
    dp.register_message_handler(send_welcome, commands=['start'], state=default_state)

    dp.register_message_handler(select_tanometr_start, Text(equals=strings.choice_tanometr_btn), state=default_state)
    dp.register_message_handler(select_tanometr_cancle, Text(equals=strings.choice_tanometr_cancle), state=SelectTanomenr.all_states)
    dp.register_message_handler(select_tanometr_cancle, commands=['cancle'], state=SelectTanomenr.all_states)
    dp.register_message_handler(select_tanometr_input, state=SelectTanomenr.waiting_for_input)


__all__ = ['register_handlers']