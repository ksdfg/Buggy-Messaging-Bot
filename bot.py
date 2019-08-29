import json
import os
import re
from collections import defaultdict as dd
from os import environ

import requests
import telebot
from emoji import demojize

import whatsapp_stuff.whatsapp as meow

# Get config data from json / env
if os.path.exists(r'whatsapp_stuff/data.json'):
    with open(r'whatsapp_stuff/data.json', 'r') as f:
        data = json.load(f)
else:
    try:
        data = {
            'api-token': environ['API_TOKEN'],
            'bot-token': environ['BOT_TOKEN'],
            'browser': environ['BROWSER'],
            'driver-path': environ['DRIVER_PATH'],
            'url': environ['API_URL'],
            'whitelist': environ['WHITELIST'].split(',')
        }
    except KeyError:
        print("You don't have configuration JSON or environment variables set, go away")
        exit(1)

bot = telebot.TeleBot(data['bot-token'])  # Create bot object

ids = dd(lambda: [])  # List of ids to send message to


# Decorator for apiorizing ids that send certain commands
def needs_authorization(func):
    def inner(message):
        if message.from_user.id in data['whitelist']:
            func(message)
        else:
            bot.reply_to(message, "I don't take orders from you, " + message.from_user.first_name)  # Lol

    return inner


def normalise(txt):
    return re.sub('^/\w+[ ,\n]', '', txt)  # To remove the /command@botname from message.text


# Just to get ids of ppl to add to whitelist
@bot.message_handler(commands=['id'])
def id(message):
    bot.reply_to(message, 'Your ID is {}'.format(message.from_user.id))


# Parikshit mode on
@bot.message_handler(commands=['start'])
def startBot(message):
    bot.reply_to(message, 'hello ladiez')


# Echo the same message back to the caller - just for fun
@bot.message_handler(commands=['echo'])
@needs_authorization
def echo(message):
    bot.send_message(message.chat.id, normalise(message.text))


# Brooklyn nine-nine needs more seasons
@bot.message_handler(commands=['coolcoolcoolcoolcool'])
def peralta(message):
    bot.reply_to(message, 'nodoubtnodoubtnodoubtnodoubtnodoubt')


# Responds to caller with the current api url from which data is requested
@bot.message_handler(commands=['showurl'])
def showURL(message):
    bot.reply_to(message, data['url'])


# Set which user ids will get the message once whatsapp is run
@bot.message_handler(commands=['setids'])
@needs_authorization
def setIDs(message):
    try:
        # Set to all - it will send to all user_ids fetched from api call to url
        ids['nyan'] = 'all' if normalise(message.text) == 'all' else list(map(int, normalise(message.text).split()))
        bot.reply_to(message, str(ids['nyan']))
    except:
        bot.reply_to(message, 'invalid ids')


# Responds to caller with the current list of names to whom message is to be sent
@bot.message_handler(commands=['showlist'])
def showlist(message):
    names, _ = meow.getData(data['url'], data['api-token'], ids['nyan'])
    bot.reply_to(message, 'names -\n\n' + '\n'.join(names))


# Start sending whatsapp message
@bot.message_handler(commands=['whatsapp'])
@needs_authorization
def startWhatsapp(message):
    """
    set the message in the format -
    Hey name :wave:
    <msg taken from command call>
    - SCRIPT bot :robot_face:
    """
    msg = (
            'Hey, {} :wave:\n' +
            demojize(normalise(message.text)) + '\n' +
            '- SCRIPT bot :robot_face:\n'
    )

    bot.reply_to(message, 'Please wait while we fetch the QR code...')

    browser = meow.startSession(data['browser'], data['driver-path'])  # Start whatsapp in selenium

    # Send qr to caller's chat
    with open(r'whatsapp_stuff/qr.png', 'rb') as qr:
        bot.send_photo(message.from_user.id, qr)
    bot.send_message(message.chat.id, 'The QR code has been sent to ' + message.from_user.first_name)

    # Wait till the text box is loaded onto the screen
    meow.waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[4]/div/div/div[1]')

    # Get data from our API
    names, numbers = meow.getData(data['url'], data['api-token'], ids['nyan'])

    # Save names of who all are gonna get messages in dogbin
    dogbin_key = json.loads(requests.post("https://del.dog/documents", '\n'.join(names)).content.decode())['key']

    # Send the url to dogbin on the chat
    bot.send_message(message.chat.id, 'The list of names that are going to get the message can be found at\n'
                                      'https://del.dog/{}'.format(dogbin_key))

    # Send messages to all entries in file
    for num, name in zip(numbers, names):
        meow.sendMessage(num, name, msg, browser)

    browser.close()  # Work done, close selenium

    # Send confirmation messages
    bot.send_message(message.chat.id, 'Messages sent!')
    print('done')


# Start ze bot

print('start')

bot.polling()
