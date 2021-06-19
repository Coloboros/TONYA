from os import stat
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text

from source.telegram_bot.bot import dp, db

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings

class SelectTanomenr(StatesGroup):
    waiting_for_input = State()

async def send_welcome(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(strings.start_content, parse_mode='MarkdownV2', reply_markup=ReplyKeyboardRemove())
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2')
    await SelectTanomenr.next()

async def select_tanometr_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.choice_tanometr_cancle)
    await message.answer(strings.choice_tanometr, parse_mode='MarkdownV2', reply_markup=kb)
    await SelectTanomenr.next()

async def select_tanometr_input(message: types.Message, state: FSMContext):
    await message.answer(strings.choice_tanometr_finish, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

async def select_tanometr_cancle(message: types.Message, state: FSMContext):
    await message.answer(strings.choice_tanometr_cancle, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'], state=default_state)
    dp.register_message_handler(select_tanometr_start, Text(equals=strings.choice_tanometr_btn), state=default_state)
    dp.register_message_handler(select_tanometr_input, state=SelectTanomenr.waiting_for_input)
    dp.register_message_handler(select_tanometr_cancle, state=SelectTanomenr.all_states)



__all__ = ['register_handlers_general']