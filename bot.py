import json

import telebot
import whatsapp_stuff.whatsapp as meow

with open(r'whatsapp_stuff\data.json', 'r') as f:
    data = json.load(f)

bot = telebot.TeleBot(data['bot-token'])


@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.reply_to(message, 'hello ladiez')
    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(data['chat-id'], qr)


@bot.message_handler(commands=['stop'])
def stopBot(message):
    bot.stop_polling()
    exit(0)


@bot.message_handler(commands=['whatsapp'])
def startWhatsapp(message):
    browser = meow.startSession()
    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(data['chat-id'], qr)
    input('meow')
    browser.close()


bot.polling()
