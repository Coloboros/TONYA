import os
from importlib import import_module

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
    handlers_dir_name = 'handlers'
    handlers_path = os.path.join(os.path.dirname(__file__), handlers_dir_name)
    print(handlers_path)

    for module in os.listdir(handlers_path):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        module_name = 'source.telegram_bot.' + handlers_dir_name + '.' + module[:-3]
        md = import_module(module_name)
        md.register_handlers(dp)
        del md

    executor.start_polling(dp, skip_updates=True)

__all__ = ['run_bot', 'db', 'dp']