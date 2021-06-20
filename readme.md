# Uroboros 2.0: Кейс MIAC

## О проекте

проект состоит из 2 среверов, сервер для хранения каких-то данных и доступа докторам к веб-сервису, и сервер обрабатывающий логику ботов

## Запуск


Заполнить settings в tonya_bot/source/settings.py и tonya_server/source/settings.py

По настройкам видно что нужна Postgres база данных

Создание сред с помощью python -m venv venv && pip install -r requirements.txt в tonya_bot и tonya_server

## Запуск ботов

В среде выполнить *export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key"

Подробнее https://cloud.google.com/speech-to-text/docs/quickstart-protocol

В среде tonya_bot запуск *python tonya_bot/bot.py*

## Запуск сервера

В среде tonya_bot запуск *gunicorn --bind 0.0.0.0:0000 app:app*

0.0.0.0:0000 - где 0.0.0.0 это хост указанный в настройках ботов, 0000 порт
