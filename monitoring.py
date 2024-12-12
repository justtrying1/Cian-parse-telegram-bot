import telebot
import json
bot = telebot.TeleBot(token="7750825181:AAFQX41MSanCjkfvxzJm_isfZW-Zr7kgsQo")
import time 
import traceback
while True:
        try:

            with open("123123.json", 'r', encoding='utf-8') as file:
                filefile =  json.load(file)
                l1 = len(filefile)
            time.sleep(600)
            with open("123123.json", 'r', encoding='utf-8') as file:
                filefile =  json.load(file)
                if l1 == len(filefile):
                    bot.send_message(7494874190, "Bot is not running")
                #filefile[len(list(filefile.keys()))] = 2
            
        except:
            print(traceback.format_exc())
    
