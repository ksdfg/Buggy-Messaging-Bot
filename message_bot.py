import json
import time

import requests
from emoji import emojize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import heroku

whatsapp_api = (
    'https://api.whatsapp.com/send?phone=91'
)  # format of url to open chat with someone

# what to send
message = (
    'Hey, {} :wave:'
    '\nThis is to remind you that *Ready Set Code* is tomorrow at *3:30pm*! '
    'Please report to _D building 2nd Floor_ with your QR code :smiley:'
    '\nIf you have a laptop, and wish to use your own net, please report to _D401_ :sunglasses:'
    '\nSee you tomorrow! :v:\n- SCRIPT bot 🤖\n'
)


def waitTillElementLoaded(browser, element):
    try:
        element_present = ec.presence_of_element_located((By.XPATH, element))
        WebDriverWait(browser, 10000).until(element_present)
    except TimeoutException:
        print('Timed out waiting for page to load')


# method to send a message to someone
def sendMessage(num, name, browser):
    api = whatsapp_api + str(num)  # specific url
    print(api, name)
    browser.get(api)  # open url in browser

    waitTillElementLoaded(
        browser, '//*[@id="action-button"]'
    )  # wait till send message button is loaded
    browser.find_element_by_xpath(
        '//*[@id="action-button"]'
    ).click()  # click on "send message" button

    # wait till the text box is loaded onto the screen, then type out and send the full message
    waitTillElementLoaded(
        browser, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'
    )

    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'
    ).send_keys(emojize(message.format(name), use_aliases=True))

    time.sleep(4)  # just so that we can supervise, otherwise it's too fast


if __name__ == '__main__':

    names = []  # list of all names
    numbers = []  # list of all numbers

    # get data from heroku
    data = json.loads(requests.get(heroku.url, headers={'Authorization': heroku.token}, ).text)

    ids_to_send = [2, 3, 9, 10, 11, 12, 13, 16, 20, 21, 22, 27, 28, 32, 34, 36, 40, 47, 50, 55, 58, 59, 62, 64, 68, 69, 74, 78, 80, 81, 82, 83, 94]


    # add names and numbers to respective lists
    for user_id in data:
        if user_id in ids_to_send:
            names.append(data[user_id]['name'])
            numbers.append(data[user_id]['phone'].split('|')[-1])

    # create a browser instance, login to whatsapp (one time per run)
    webbrowser = webdriver.Firefox(executable_path='geckodriver.exe')
    webbrowser.get('https://web.whatsapp.com/')

    # wait till the text box is loaded onto the screen
    waitTillElementLoaded(webbrowser, '/html/body/div[1]/div/div/div[4]/div/div/div[1]')
    
    # send messages to all entries in file
    for num, name in zip(numbers, names):
        sendMessage(num, name, webbrowser)

    webbrowser.close()  # close browser
