
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

d = load_parameters()
b = 1

for i in list(d.values()):
    
    try:
        print(i['sex'])
        bot.send_message(i['chat_id'], "Я случайно удалил ровно половину пользовательских данных :) поэтому если у вас есть знакомые которые пользовались ботом, то скажите им об этом, если вы получили это сообщение, значит ваши данные у меня остались. ")
    except Exception as e:
        
        print(e)
print(b)