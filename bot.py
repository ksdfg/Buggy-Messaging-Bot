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
    bot.reply_to(message, 'Please wait while we fetch the qr code...')

    browser = meow.startSession(data['browser'])
    browser.minimize_window()

    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(message.from_user.id, qr)

    # wait till the text box is loaded onto the screen
    meow.waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[4]/div/div/div[1]')

    with open(r'whatsapp_stuff\msg.txt', 'r') as msg:
        meow.sendMessage(9011152660, 'ksdfg', msg.read(), browser)

    browser.close()


bot.polling()
