from telegrambot import filter_ads, load_ads, load_parameters, parse_addon
API_TOKEN = '7535762439:AAFtiztp9pG3JsPnX7T7IRjuB6cQtqe5sno'
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
import traceback

#API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

ads_to_filter = []
ads = load_ads()
for segment in ads:

    for ad in ads[segment]:
        if 'addon' in ad:
            ads_to_filter = ads_to_filter + [ad]


params = load_parameters()
params = params["7494874190"]
filtered_ads = filter_ads(ads_to_filter, params)
for ad in filtered_ads[-20:]:
    msg = f"""{ad['title']}
🚇Метро: {ad['underground']} {ad['metro_dist']}
🧍‍♂️Автор: {ad['author_type']}
💸Цена: {ad['price_per_month']}₽
🏘Район: {ad['district']}
🔗Источник: {ad['url']}\n
"""
    
    if 'addon' in ad:
        parsed_addon = parse_addon(ad['addon'], params=params, good_description=ad['good_description'])
    
        msg = msg + parsed_addon  
                #  import pdb; pdb.set_trace()
    else:
        parsed_addon = ""
    if parsed_addon != "":
        bot.send_message(params['chat_id'], msg)