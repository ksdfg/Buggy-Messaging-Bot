import json

import telebot

with open(r'whatsapp-stuff\data.json', 'r') as f:
    data = json.load(f)

bot = telebot.TeleBot(data['bot-token'])


@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.reply_to(message, 'hello ladiez')
    with open(r"whatsapp-stuff\qr.png", 'rb') as qr:
        bot.send_photo(data['chat-id'], qr)


@bot.message_handler(commands=['stop'])
def stopBot(message):
    bot.stop_polling()
    exit(0)


bot.polling()
