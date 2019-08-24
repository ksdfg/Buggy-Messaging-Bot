import time

import pandas as pd
from emoji import emojize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

whatsapp_api = "https://api.whatsapp.com/send?phone=91"  # format of url to open chat with someone

hello = "Hey, {} :wave:"  # what to print before name

# what to print after name
message = "\nThis is to remind you that *Ready Set Code* is tomorrow at *3:30pm*! " \
          "Please report to _D building 2nd Floor_ with your QR code :smiley:" \
          "\nIf you have a laptop, and wish to use your own net, please report to _D401_ :sunglasses:" \
          "\nSee you tomorrow! :v:\n- The Script Group bot 🤖\n"


# method to send a message to someone
def sendMessage(num, name, browser):
    api = whatsapp_api + str(num)  # specific url
    final = emojize(hello.format(name) + message, use_aliases=True)  # full message with name
    print(api, name)
    browser.get(api)  # open url in browser
    browser.find_element_by_xpath('//*[@id="action-button"]').click()  # click on "send message" button

    # wait till the text box is loaded onto the screen
    try:
        element_present = ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer'
                                                                    '/div[1]/div[2]/div/div[2]'))
        WebDriverWait(browser, 10000).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # type out and send the full message
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'
    ).send_keys(final)

    time.sleep(5)  # just so that we can supervise, otherwise it's too fast


if __name__ == "__main__":
    # read all entries to send message to
    excel = pd.read_excel("Tests.xlsx")
    numbers = excel['Number'].tolist()
    names = excel['Name'].tolist()

    # create a browser instance, login to whatsapp (one time per run)
    webbrowser = webdriver.Firefox(executable_path='geckodriver.exe')
    webbrowser.get('https://web.whatsapp.com/')
    input('\npress enter when whatsapp login is done\n')

    # send messages to all entries in file
    for num, name in zip(numbers, names):
        sendMessage(num, name, webbrowser)

    webbrowser.close()  # close browser
