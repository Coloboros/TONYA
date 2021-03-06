from os import stat
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types import message
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text


from source.lib.aiogram_calendar import dialog_cal_callback, DialogCalendar

from source.telegram_bot.bot import db, dp

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings
from source.settings import SERVER_HOST_AUTH_URL, SERVER_HOST_PROTOCOL, SERVER_HOST


import requests
import json

req_headers_json = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class PropertyStates(StatesGroup):
    waiting_for_birthday = State()
    waiting_for_height = State()
    waiting_for_width = State()

async def set_property_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.set_property_cancle_btn)

    await message.answer(strings.set_property, reply_markup=kb)
    await message.answer(strings.set_property_start, reply_markup=await DialogCalendar().start_calendar())
    await PropertyStates.next()

async def set_property_cancle(message: types.Message, state: FSMContext):
    await message.answer(strings.set_property_cancle, reply_markup=home_kb(message.from_user.id))
    await state.finish()

async def set_property_input_birthday(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query)


async def set_property_input_birthday(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        data = {
            "year": date.year,
            "month": date.month,
            "day": date.day,
        }
        await state.update_data(birthday=data)

        await callback_query.message.answer(
            f'{strings.set_property_select_birthday} {date.strftime("%d/%m/%Y")}\n{strings.set_property_input_height}',
        )
        await PropertyStates.next()


async def set_property_input_height(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(height=int(message.text), user_id=message.from_user.id)
        await message.answer(strings.set_property_input_weidth)
        await PropertyStates.next()
    else:
        await message.answer(strings.set_property_input_height_invalid)

url_set_poperty = SERVER_HOST_PROTOCOL + "://" + SERVER_HOST + 'user/set-property/'

async def set_property_input_width(message: types.Message, state: FSMContext):
    if is_float(message.text):
        await state.update_data(width=float(message.text))

        response = requests.post(
            url_set_poperty ,
            data=json.dumps(await state.get_data()),
            headers=req_headers_json)

        if response.status_code != 200:
            print(url_set_poperty)
            print(response.status_code)
            print('****ERROR**** upps in general select_tanometr_input')
            print(await state.get_data())
        await message.answer(strings.set_property_select_finish, reply_markup=home_kb(message.from_user.id))
        await state.finish()
    else:
        await message.answer(strings.set_property_input_weidth_invalid)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(set_property_start, Text(equals=strings.set_property_btn), state=default_state)
    dp.register_message_handler(set_property_cancle, Text(equals=strings.set_property_cancle_btn), state=PropertyStates.all_states)
    dp.register_message_handler(set_property_cancle, commands=['cancle'], state=PropertyStates.all_states)
    dp.register_callback_query_handler(set_property_input_birthday, dialog_cal_callback.filter(), state=PropertyStates.waiting_for_birthday)
    dp.register_callback_query_handler(set_property_cancle, lambda cb: False, state=PropertyStates.waiting_for_birthday)
    dp.register_message_handler(set_property_input_height, state=PropertyStates.waiting_for_height)
    dp.register_message_handler(set_property_input_width, state=PropertyStates.waiting_for_width)

__all__ = ['register_handlers']
