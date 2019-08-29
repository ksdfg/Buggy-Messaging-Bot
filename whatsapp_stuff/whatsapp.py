import base64
import json
import os
import re
from time import sleep

import requests
from emoji import emojize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

whatsapp_api = 'https://api.whatsapp.com/send?phone=91'  # format of url to open chat with someone

home = '' if re.match('.+whatsapp_stuff', os.getcwd()) else 'whatsapp_stuff/'

driver = {
    'firefox': [webdriver.Firefox, 'geckodriver'],
    'chrome': [webdriver.Chrome, 'chromedriver']
}


def waitTillElementLoaded(browser, element):
    try:
        element_present = ec.presence_of_element_located((By.XPATH, element))
        WebDriverWait(browser, 10000).until(element_present)
    except TimeoutException:
        print('Timed out waiting for page to load')


# method to send a message to someone
def sendMessage(num, name, msg, browser):
    api = whatsapp_api + str(num)  # specific url
    print(api, name)
    browser.get(api)  # open url in browser

    waitTillElementLoaded(browser, '//*[@id="action-button"]')  # wait till send message button is loaded
    browser.find_element_by_xpath('//*[@id="action-button"]').click()  # click on "send message" button

    # wait till the text box is loaded onto the screen, then type out and send the full message
    waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')

    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'
    ).send_keys(emojize(msg.format(name), use_aliases=True))

    sleep(3)  # just so that we can supervise, otherwise it's too fast


def startSession(browser_type, driver_path):
    browser = driver[browser_type][0](executable_path=driver_path)
    browser.get('https://web.whatsapp.com/')

    # get the qr image
    waitTillElementLoaded(browser, '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img')
    if os.path.exists(home + 'qr.png'):
        print('removing old qr')
        os.remove(home + 'qr.png')
    meow = open(home + 'qr.png', 'wb')
    meow.write(base64.b64decode(browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img').get_attribute('src')[22:]))
    meow.close()
    print('qr saved')

    return browser


def getData(url, token, ids):
    names_list = []  # list of all names
    numbers_list = []  # list of all numbers

    # get data from our API
    api_data = json.loads(requests.get(url, headers={'Authorization': token}, ).text)

    if ids == 'all':
        ids = map(int, api_data.keys())

    # add names and numbers to respective lists
    for user_id in api_data:
        if int(user_id) in ids:
            names_list.append(api_data[user_id]['name'])
            numbers_list.append(api_data[user_id]['phone'].split('|')[-1])

    return names_list, numbers_list
