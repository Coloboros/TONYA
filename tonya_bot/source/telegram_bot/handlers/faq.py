from os import stat
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text

from source.telegram_bot.bot import db

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings


class FaqStates(StatesGroup):
    waiting_for_input = State()

async def faq_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row_width = 1
    kb.add(strings.faq_contact_btn, strings.faq_cancle_btn)
    await message.answer(strings.faq_content, reply_markup=kb)
    await FaqStates.next()

async def faq_contact(message: types.Message, state: FSMContext):
    await message.answer(strings.faq_contact_btn, parse_mode='MarkdownV2')

async def faq_cancle(message: types.Message, state: FSMContext):
    await message.answer(strings.faq_cancle_btn, reply_markup=home_kb(message.from_user.id))
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(faq_start, Text(equals=strings.faq_btn), state=default_state)
    dp.register_message_handler(faq_cancle, Text(equals=strings.faq_cancle_btn, ignore_case=True), state=FaqStates.all_states)
    dp.register_message_handler(faq_contact, Text(equals=strings.faq_contact_btn, ignore_case=True), state=FaqStates.waiting_for_input)

__all__ = ['register_handlers']
