
API_TOKEN = '7535762439:AAFtiztp9pG3JsPnX7T7IRjuB6cQtqe5sno'  # Замените на ваш токен
JSON_FILE_PATH = '&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json'
import telebot
import json
import time
import os
import re
import datetime
from datetime import timedelta
from datetime import datetime
from copy import deepcopy
from telebot import types

#API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

from telegrambot import load_parameters

a = load_parameters()

b = 1

for i in list(a.values()):
    try:
        if i['chat_id'] == 7494874190:
            b = b+10
            bot.send_message(i['chat_id'], "test")
    except Exception as e:
        b = b+1
        print(e)
print(b)