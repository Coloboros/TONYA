from os import stat
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types import reply_keyboard
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text


from source.lib.aiogram_calendar import dialog_cal_callback, DialogCalendar
from source.lib.aiogram_calendar import month_cal_callback, MonthCalendar
from source.lib.aiogram_calendar import year_cal_callback, YearCalendar

from source.telegram_bot.bot import db, dp

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings
from source.settings import SERVER_HOST_AUTH_URL, SERVER_HOST_PROTOCOL

import requests
import json

class ShowGraphicsStates(StatesGroup):
    waiting_for_choice_type = State()
    waiting_for_input_day = State()
    waiting_for_input_month = State()
    waiting_for_input_year = State()

async def show_graphics_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row_width = 1
    kb.add(
        strings.show_graphics_choice_day_btn,
        strings.show_graphics_choice_month_btn,
        strings.show_graphics_choice_year_btn,
        strings.show_graphics_cancle_btn)

    await message.answer(strings.show_graphics, reply_markup=kb)
    await ShowGraphicsStates.next()

async def show_graphics_cancle(message: types.Message, state: FSMContext):
    await message.answer(strings.show_graphics_cancle, reply_markup=home_kb(message.from_user.id))
    await state.finish()


async def show_graphics_choice_day(message: types.Message, state: FSMContext):
    await message.answer(strings.show_graphics_choice_day, reply_markup=await DialogCalendar().start_calendar())
    await ShowGraphicsStates.next()

async def show_graphics_choice_month(message: types.Message, state: FSMContext):
    await message.answer(strings.show_graphics_choice_month, reply_markup=await MonthCalendar().start_calendar())
    await ShowGraphicsStates.next()
    await ShowGraphicsStates.next()

async def show_graphics_choice_year(message: types.Message, state: FSMContext):
    await message.answer(strings.show_graphics_choice_year, reply_markup=await YearCalendar().start_calendar())
    await ShowGraphicsStates.next()
    await ShowGraphicsStates.next()
    await ShowGraphicsStates.next()

async def show_graphics_input_day(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'{date.strftime("%d/%m/%Y")}',
        )
        await finish(callback_query, state)

async def show_graphics_input_month(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await MonthCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'{date.strftime("%d/%m/%Y")}',
        )
        await finish(callback_query, state)

async def show_graphics_input_year(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await YearCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'{date.strftime("%d/%m/%Y")}',
        )
        await finish(callback_query, state)

async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer(strings.show_graphics_choice_finish, reply_markup=home_kb(callback_query.message.from_user.id))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_graphics_start, Text(equals=strings.show_graphics_btn), state=default_state)
    dp.register_message_handler(show_graphics_cancle, Text(equals=strings.show_graphics_cancle_btn), state=ShowGraphicsStates.all_states)
    dp.register_message_handler(show_graphics_cancle, commands=['cancle'], state=ShowGraphicsStates.all_states)

    dp.register_message_handler(show_graphics_choice_day, Text(equals=strings.show_graphics_choice_day_btn), state=ShowGraphicsStates.waiting_for_choice_type)
    dp.register_message_handler(show_graphics_choice_month, Text(equals=strings.show_graphics_choice_month_btn), state=ShowGraphicsStates.waiting_for_choice_type)
    dp.register_message_handler(show_graphics_choice_year, Text(equals=strings.show_graphics_choice_year_btn), state=ShowGraphicsStates.waiting_for_choice_type)

    dp.register_callback_query_handler(show_graphics_input_day, dialog_cal_callback.filter(), state=ShowGraphicsStates.waiting_for_input_day)
    dp.register_callback_query_handler(show_graphics_input_month, month_cal_callback.filter(), state=ShowGraphicsStates.waiting_for_input_month)
    dp.register_callback_query_handler(show_graphics_input_year, year_cal_callback.filter(), state=ShowGraphicsStates.waiting_for_input_year)

__all__ = ['register_handlers']
