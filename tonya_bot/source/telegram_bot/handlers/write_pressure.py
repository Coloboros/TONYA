import json
from os import stat, wait
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text

from source.settings import SERVER_HOST_AUTH_URL, SERVER_HOST_PROTOCOL, SERVER_HOST

from google.cloud import speech # type: ignore
import requests
import re

from source.telegram_bot.bot import dp, db, bot

from source.telegram_bot.kb import home_kb
import source.telegram_bot.strings as strings


req_headers_json = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Получение текста из файла расположенного по ссылке
def get_text_from_voice_url(file_url):
    # Получение данных голосового сообщения в виде бинарного кода из ссылки
    answer = requests.get(file_url)
    # Инициализирование клиента для распознования текста из голосового сообщения 
    client = speech.SpeechClient()
    # Помещение бинарных данных как интересуемый контент
    audio = speech.RecognitionAudio(content=answer.content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code="ru-RU",
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript

# Наождение цифр в сроке
def find_numbers(sentence):
    words = re.findall(r'\d+', sentence)
    return [int(word) for word in words if word.isdigit()]

# Есть ли в строке 3 числа
def check_messge_val(text):
    vals = find_numbers(text)
    return len(vals) == 3

# Класс состояний
class WritePressure(StatesGroup):
    waiting_for_val = State()
    waiting_for_accept = State()
    waiting_for_tags = State()

# Начала сценария сбора показателй танометра
async def write_pressure_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(strings.write_pressure_cancle_btn)
    await message.answer(strings.write_pressure_input_val, parse_mode='MarkdownV2', reply_markup=kb)
    await WritePressure.next()

# Обработка текста показаний
async def write_pressure_input_val(message: types.Message, state: FSMContext):
    vals = find_numbers(message.text)
    if (len(vals) == 3):

        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('Бег', 'Подъём по лестнице', 'Долгая прогулка')
        kb.row(strings.write_pressure_cancle_btn)

        await message.answer(strings.write_pressure_input_tags, parse_mode='MarkdownV2', reply_markup=kb)
        # запись значений танометра в переменную состояния
        await state.update_data(vals=vals)
        await WritePressure.next()
        await WritePressure.next()
    else:
        await message.answer(strings.write_pressure_input_val_invalid)

# Обработка голосового сосбщения с показаниями
async def voice_message(message: types.Message, state:FSMContext):
    # Получение ссылки на файл голосового сообщения
    file_url = await message.voice.get_url()
    # Получение текста из голосового сообщения
    text = get_text_from_voice_url(file_url)

    # Флаг проверки корректности текста голосового сообщения
    f = check_messge_val(text)

    ikb = InlineKeyboardMarkup()
    ikb.row_width = 1
    ikb.add(
        InlineKeyboardButton("Потвердить", callback_data='accept'),
        InlineKeyboardButton("Внести заново", callback_data='repiat'))
    
    # Случаи при корректности текста голосового сообщения
    if f:
        vals = find_numbers(text)
        await message.answer("Вы сказали: {}".format(text), reply_markup=ikb)
        # запись значений танометра в переменную состояния
        await state.update_data(vals=vals)
        await WritePressure.next()
    else:
        await message.answer("Вы сказали: {}".format(text))
        await message.answer(strings.write_pressure_input_val_invalid)

# Обработчик подтвержедения корректности голосового сообщения
async def callback_accapet(callback_query: types.CallbackQuery, state:FSMContext):
    chat_id = callback_query.message.chat.id
    msg_id = callback_query.message.message_id
    await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=InlineKeyboardMarkup())
    await callback_query.answer(strings.write_pressure_input_tags)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Бег', 'Подъём по лестнице', 'Долгая прогулка')
    kb.row(strings.write_pressure_cancle_btn)

    await callback_query.message.answer(strings.write_pressure_input_tags, reply_markup=kb)
    await WritePressure.next()

# Обработчик повтора ввода данных танометра
async def callback_repiat(callback_query: types.CallbackQuery, state:FSMContext):
    chat_id = callback_query.message.chat.id
    msg_id = callback_query.message.message_id
    await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=InlineKeyboardMarkup())
    await callback_query.answer(strings.write_pressure_input_val_invalid)
    await callback_query.message.answer(strings.write_pressure_input_val_invalid)
    await WritePressure.previous()

url_create_tonometr_report = SERVER_HOST_PROTOCOL + "://" + SERVER_HOST + 'user/set-tonometr-report/'

# Обработчик ввода тега с последующей отправкой данных на сервер и выходом из состояния пользователем 
async def write_pressure_input_tags(message: types.Message, state: FSMContext):
    await state.update_data(tags=message.text)
    await state.update_data(user_id=message.from_user.id)
    await message.answer(strings.write_pressure_finish, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))


    response = requests.post(
        url_create_tonometr_report ,
        data=json.dumps(await state.get_data()),
        headers=req_headers_json)

    await state.finish()

async def write_pressure_cancle(message: types.Message, state:FSMContext):
    await message.answer(strings.write_pressure_cancle, parse_mode='MarkdownV2', reply_markup=home_kb(message.from_user.id))
    await state.finish()

async def write_pressure_accept(message: types.Message, state:FSMContext):
    await WritePressure.next()

def tmp(cb):
    print(cb.data)
    return False

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(write_pressure_start, Text(equals=strings.write_pressure_btn), state=default_state)
    dp.register_message_handler(write_pressure_cancle, Text(equals=strings.write_pressure_cancle_btn), state=WritePressure.all_states)
    dp.register_message_handler(write_pressure_cancle, commands=['cancle'], state=WritePressure.all_states)
    dp.register_message_handler(write_pressure_input_val, state=WritePressure.waiting_for_val)
    dp.register_message_handler(voice_message, content_types=ContentType.VOICE, state=WritePressure.waiting_for_val)
    dp.register_message_handler(write_pressure_input_tags, state=WritePressure.waiting_for_tags)

    dp.register_callback_query_handler(callback_accapet, lambda cb: cb.data == "accept", state=WritePressure.waiting_for_accept)
    dp.register_callback_query_handler(callback_repiat, lambda cb: cb.data == "repiat", state=WritePressure.waiting_for_accept)


__all__ = ['register_handlers']
