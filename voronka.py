BOT_KEY = "7269007085:AAEiADvC61at6sgE2CcAtzQMPXHCWipGz5A"

import telebot
bot = telebot.TeleBot(BOT_KEY)
@bot.message_handler(commands=['start'])
def buy(message):
    try:
        bot.send_message(message.chat.id, "https://flatoon.ru")
    except:
        pass
bot.polling()