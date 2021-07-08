# Импорты
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

# заголовок для наших запросов на сервер
req_headers_json = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

# Класс состояний
class SelectTanomenr(StatesGroup):
    waiting_for_input = State()

# Вход в состояние SelectTanomenr, при запуске бота в первый раз
async def send_welcome(message: types.Message):
    # тело запроса на сервер
    data = {
        "bot_type": "telegram",
        "user_id": str(message.from_user.id)
    }

    # запрос на сервер, для регистрации пользователя в бд
    response = requests.post(
        SERVER_HOST_PROTOCOL + "://" + SERVER_HOST_AUTH_URL,
        data=json.dumps(data),
        headers=req_headers_json)

    # Вывод сообщений ботом
    await message.answer(strings.start_content, reply_markup=ReplyKeyboardRemove())
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2')
    await SelectTanomenr.next()

# Вход в состояние SelectTanomenr
async def select_tanometr_start(message: types.Message):
    # Создание клавиатуры для пользователя
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.choice_tanometr_cancle)
    # Вывод сообщения ботом с созданной ранее клавиатуры
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2', reply_markup=kb)
    # Регистрация нового состояния пользователя
    await SelectTanomenr.next()

# Формирование ссылки для отправки даных о танометре пользователя на сервер
url_set_tonometr = SERVER_HOST_PROTOCOL + "://" + SERVER_HOST + 'user/set-tonometr/'

# Выбор танометра
async def select_tanometr_input(message: types.Message, state: FSMContext):
    # тело запроса на сервер
    data = {
        "bot_type": "telegram",
        "user_id": str(message.from_user.id),
        "tonometr": message.text
    }
    # Запрос на сервер, для регистрации текущего танометра пользователя в бд
    response = requests.post(
        url_set_tonometr,
        data=json.dumps(data),
        headers=req_headers_json)

    # Вывод сообщений ботом
    await message.answer(strings.choice_tanometr_finish, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    # Выход пользователя из текущего состояния
    await state.finish()

# Отмена изменения танометра
async def select_tanometr_cancle(message: types.Message, state: FSMContext):
    # Вывод сообщений ботом
    await message.answer(strings.choice_tanometr_cancle, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    # Выход пользователя из текущего состояния
    await state.finish()

# Информирование о окончания данной операции, с измением клавиатуры пользователя 
async def home_cmd(message: types.Message):
    await message.answer(strings.main_menu, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))


# регистрация всех обрабочиков сообщений
def register_handlers(dp: Dispatcher):
    # регистрация обработчика, реагирующий когда пользователь не имеет состояний на команду home, вызывает метод home_cmd
    dp.register_message_handler(home_cmd, commands=['home'], state=default_state)
    # регистрация обработчика, реагирующий когда пользователь не имеет состояний на команду start, что является первым сообщением боту, вызывает метод send_welcome
    dp.register_message_handler(send_welcome, commands=['start'], state=default_state)
    
    # Регистрация обработчика, реагирующий когда пользователь не имеет состояний 
    # на текст хранящийся в strings.choice_tanometr_btn, вызывает метод select_tanometr_start
    dp.register_message_handler(select_tanometr_start, Text(equals=strings.choice_tanometr_btn), state=default_state)
    # Регистрация обработчика, реагирующий когда пользователь в любом состоянии SelectTanomenr 
    # на текст хранящийся в strings.choice_tanometr_cancle, вызывает метод select_tanometr_cancle
    dp.register_message_handler(select_tanometr_cancle, Text(equals=strings.choice_tanometr_cancle), state=SelectTanomenr.all_states)
    # Регистрация обработчика, реагирующий когда пользователь в любом состоянии SelectTanomenr
    # на команду cancle, вызывает метод select_tanometr_cancle
    dp.register_message_handler(select_tanometr_cancle, commands=['cancle'], state=SelectTanomenr.all_states)
    # Регистрация обработчика, реагирующий когда пользователь в waiting_for_input состояния SelectTanomenr
    # на любой текст, вызывает метод select_tanometr_input
    dp.register_message_handler(select_tanometr_input, state=SelectTanomenr.waiting_for_input)


__all__ = ['register_handlers']
