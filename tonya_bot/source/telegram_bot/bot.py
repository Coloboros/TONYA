import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ..settings import BOT_TOKEN
from ..db import DataBase
from . import strings



logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase()


def run_bot():

    from source.telegram_bot.handlers.general import register_handlers_general
    from source.telegram_bot.handlers.faq import register_handlers_faq
    from source.telegram_bot.handlers.write_pressure import register_handlers_write_pressure

    register_handlers_faq(dp)
    register_handlers_general(dp)
    register_handlers_write_pressure(dp)

    executor.start_polling(dp, skip_updates=True)

__all__ = ['run_bot', 'db', 'dp']