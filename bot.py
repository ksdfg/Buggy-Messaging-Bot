import json
import os
import re
from collections import defaultdict as dd
from os import environ

import requests
import telebot
from emoji import demojize

import whatsapp_stuff.whatsapp as meow

if os.path.exists(r'whatsapp_stuff\data.json'):
    with open(r'whatsapp_stuff\data.json', 'r') as f:
        data = json.load(f)
else:
    try:
        data = {
            'auth-token': environ['AUTH_TOKEN'],
            'bot-token': environ['BOT_TOKEN'],
            'browser': environ['BROWSER'],
            'driver-path': environ['DRIVER_PATH'],
            'url': environ['API_URL'],
            'whitelist': environ['WHITELIST']
        }
    except KeyError:
        print("You don't have configuration JSON or environment variables set, go away")
        exit(1)


bot = telebot.TeleBot(data['bot-token'])

ids = dd(lambda: [])


def needs_authorization(func):
    def inner(message):
        if message.from_user.id in data['whitelist']:
            func(message)
        else:
            bot.reply_to(message, 'get rekt noob')

    return inner


def normalise(txt):
    return re.sub('^/\w+[ ,\n]', '', txt)


@bot.message_handler(commands=['id'])
def id(message):
    bot.reply_to(message, 'Your ID is {}'.format(message.from_user.id))


@bot.message_handler(commands=['start'])
def startBot(message):
    bot.reply_to(message, 'hello ladiez')


@bot.message_handler(commands=['say'])
@needs_authorization
def echo(message):
    bot.send_message(message.chat.id, normalise(message.text))


@bot.message_handler(commands=['coolcoolcoolcoolcool'])
def peralta(message):
    bot.reply_to(message, 'nodoubtnodoubtnodoubtnodoubtnodoubt')


@bot.message_handler(commands=['showurl'])
def showURL(message):
    bot.reply_to(message, data['url'])


@bot.message_handler(commands=['setids'])
@needs_authorization
def setIDs(message):
    try:
        ids['nyan'] = 'all' if normalise(message.text) == 'all' else list(map(int, normalise(message.text).split()))
        bot.reply_to(message, str(ids['nyan']))
    except:
        bot.reply_to(message, 'invalid ids')


@bot.message_handler(commands=['showids'])
def showIDs(message):
    bot.reply_to(message, str(ids['nyan']))


@bot.message_handler(commands=['whatsapp'])
@needs_authorization
def startWhatsapp(message):
    msg = (
            'Hey, {} :wave:\n' +
            demojize(normalise(message.text)) + '\n' +
            '- Team SCRIPT :v:\n'
    )

    bot.reply_to(message, 'Please wait while we fetch the qr code...')

    browser = meow.startSession(data['browser'], data['driver-path'])

    with open(r'whatsapp_stuff\qr.png', 'rb') as qr:
        bot.send_photo(message.chat.id, qr)

    # wait till the text box is loaded onto the screen
    meow.waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[4]/div/div/div[1]')

    # get data from our API
    names, numbers = meow.getData(data['url'], data['auth-token'], ids['nyan'])

    dogbin_key = json.loads(requests.post("https://del.dog/documents", names).content.decode())['key']

    bot.send_message(message.chat.id, 'The list of names that are going to get the message can be found at\n'
                                      'https://del.dog/{}'.format(dogbin_key))

    # send messages to all entries in file
    for num, name in zip(numbers, names):
        meow.sendMessage(num, name, msg, browser)

    browser.close()

    bot.send_message(message.chat.id, 'Messages sent!')
    print('done')


print('start')

bot.polling()
