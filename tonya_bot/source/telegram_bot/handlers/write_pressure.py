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

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class WritePressure(StatesGroup):
    waiting_for_val = State()
    waiting_for_tags = State()

async def write_pressure_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.write_pressure_cancle_btn)
    await message.answer(strings.write_pressure_input_val, parse_mode='MarkdownV2', reply_markup=kb)
    await WritePressure.next()

async def write_pressure_input_val(message: types.Message):
    vals = message.text.strip().split(' ')
    is_ints = all([is_int(val) for val in vals])
    if (len(vals) != 3 or not is_ints):
        await message.answer(strings.write_pressure_input_val_invalid)
    else:
        await message.answer(strings.write_pressure_input_tags, parse_mode='MarkdownV2')
        await WritePressure.next()

async def write_pressure_input_tags(message: types.Message, state: FSMContext):
    await message.answer(strings.write_pressure_finish, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(write_pressure_start, Text(equals=strings.write_pressure_btn), state=default_state)
    dp.register_message_handler(write_pressure_input_val, state=WritePressure.waiting_for_val)
    dp.register_message_handler(write_pressure_input_tags, state=WritePressure.waiting_for_tags)



__all__ = ['register_handlers']