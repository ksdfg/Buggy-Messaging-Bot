import json

import telebot

import whatsapp_stuff.whatsapp as meow
from emoji import demojize

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


@bot.message_handler(commands=['setids'])
def setIDs(message):
    try:
        data['ids'] = list(map(int, message.text[8:].split()))
        bot.reply_to(message, str(data['ids']))
    except:
        bot.reply_to(message, 'invalid ids')


@bot.message_handler(commands=['showids'])
def showIDs(message):
    bot.reply_to(message, str(data['ids']))


@bot.message_handler(commands=['whatsapp'])
def startWhatsapp(message):
    msg = (
            'Hey, {} :wave:\n' +
            demojize(message.text[10:]) + '\n' +
            '- Team SCRIPT :v:\n'
    )

    bot.reply_to(message, 'Please wait while we fetch the qr code...')

    browser = meow.startSession(data['browser'])
    browser.minimize_window()

    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(message.from_user.id, qr)

    # wait till the text box is loaded onto the screen
    meow.waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[4]/div/div/div[1]')

    # get data from heroku
    names, numbers = meow.getData(data['url'], data['auth-token'], data['ids'])

    # send messages to all entries in file
    for num, name in zip(numbers, names):
        meow.sendMessage(num, name, msg, browser)

    browser.close()

    bot.send_message(message.from_user.id, 'Messages sent!')
    print('done')


bot.polling()
