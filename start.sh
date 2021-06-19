#!/bin/bash

(./tonya_server/venv/bin/python tonya_server/app.py &&) || (./tonya_bot/venv/bin/python tonya_bot/bot.py &&)