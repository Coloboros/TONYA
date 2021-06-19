from os import stat
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text

from source.telegram_bot.bot import db

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings
from source.settings import SERVER_HOST_AUTH_URL, SERVER_HOST_PROTOCOL

import requests
import json

req_headers = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

class AuthStates(StatesGroup):
    waiting_for_auth = State()

async def auth_start(message: types.Message):
    data = {
        "bot_type": "telegram",
        "user_id": str(message.from_user.id)
    }

    print(SERVER_HOST_PROTOCOL + "://" + SERVER_HOST_AUTH_URL)
    response = requests.post(
        SERVER_HOST_PROTOCOL + "://" + SERVER_HOST_AUTH_URL,
        data=json.dumps(data),
        headers=req_headers)

    print(response.json())
    if response.status_code == 200:
        return


    await message.answer(strings.auth, parse_mode='MarkdownV2', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'<a href="{SERVER_HOST_AUTH_URL}">{SERVER_HOST_AUTH_URL}</a>', parse_mode=types.ParseMode.HTML)

    await AuthStates.next()

async def faq_contact(message: types.Message, state: FSMContext):
    await message.answer(f'<a href="{SERVER_HOST_AUTH_URL}">{SERVER_HOST_AUTH_URL}</a>', parse_mode=types.ParseMode.HTML)
    # await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(auth_start, Text(equals=strings.auth_btn), state=default_state)

__all__ = ['register_handlers']
