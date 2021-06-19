from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
import source.telegram_bot.strings as strings
from source.telegram_bot.bot import db


def home_kb(user_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row_width = 1
    kb.add(strings.write_pressure_btn)
    kb.add(strings.choice_tanometr_btn)
    kb.add(strings.faq_btn)
    kb.add(strings.auth_btn)

    return kb
