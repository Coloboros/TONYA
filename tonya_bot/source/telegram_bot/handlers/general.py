from os import stat
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

from source.voice_settings import YANDEX_KEY, VOICE_LANGUAGE, MAX_MESSAGE_SIZE, MAX_MESSAGE_DURATION
from source.settings import BOT_TOKEN

from google.cloud import speech

async def voice_message(message: types.Message):
    data = message.voice
    file_url = await data.get_url()

    client = speech.SpeechClient()
    # [END speech_python_migration_client]

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=file_url)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code="ru-RU",
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        await message.answer("Transcript: {}".format(result.alternatives[0].transcript))

async def home_cmd(message: types.Message):
    await message.answer(strings.main_menu, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(home_cmd, commands=['home'], state=default_state)
    dp.register_message_handler(send_welcome, commands=['start'], state=default_state)

    dp.register_message_handler(select_tanometr_start, Text(equals=strings.choice_tanometr_btn), state=default_state)
    dp.register_message_handler(select_tanometr_cancle, Text(equals=strings.write_pressure_cancle_btn), state=SelectTanomenr.all_states)
    dp.register_message_handler(select_tanometr_cancle, commands=['cancle'], state=SelectTanomenr.all_states)
    dp.register_message_handler(select_tanometr_input, state=SelectTanomenr.waiting_for_input)

    dp.register_message_handler(voice_message, content_types=ContentType.VOICE, state=default_state)


__all__ = ['register_handlers']