import json

import telebot
import whatsapp_stuff.whatsapp as meow

with open(r'whatsapp_stuff\data.json', 'r') as f:
    data = json.load(f)

bot = telebot.TeleBot(data['bot-token'])


@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.reply_to(message, 'hello ladiez')


@bot.message_handler(commands=['stop'])
def stopBot(message):
    bot.stop_polling()
    exit(0)


@bot.message_handler(commands=['whatsapp'])
def startWhatsapp(message):
    browser = meow.startSession(data['browser'])
    browser.minimize_window()
    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(message.from_user.id, qr)
    input('meow')
    browser.close()


bot.polling()
