import pyautogui as py
import pandas as pd
import time

whatsapp_api = "https://api.whatsapp.com/send?phone=91"
hello = "Bleep Bloop, I'm a bot\nHey, "

message = "This is to remind you that Ready Set Code is tomorrow at 3:30pm!" \
          " Location will be given out soon (Most probably in D-building, 3rd floor)." \
          "\nSee you tomorrow! :)\n- The Script Group"


def timer():
    for x in range(5, 0, -1):
        print(x)
        time.sleep(1)


def sendMessage(num, name):
    api = whatsapp_api + str(num)
    final = hello + name + "!\n" + message
    print(api, name)
    py.hotkey('ctrl', 't')
    time.sleep(1)
    py.typewrite(api, interval=0.01)
    py.press('enter')
    time.sleep(3)
    py.press(['\t', '\t', 'enter'])
    while True:
        if py.getWindowsWithTitle(') Whatsapp'):
            break
        time.sleep(0.2)
    time.sleep(4)
    py.typewrite(final, interval=0.01)
    py.press('enter')
    time.sleep(5)
    py.hotkey('ctrl', 'w')


if __name__ == "__main__":
    timer()
    py.getWindowsWithTitle('Mozilla Firefox')[0].activate()
    excel = pd.read_excel("Tests.xlsx")
    numbers = excel['Number'].tolist()
    names = excel['Name'].tolist()
    ctr = 0

    for num, name in zip(numbers, names):
        sendMessage(num, name)
        ctr += 1
        if ctr == 30:
            break

    py.hotkey('win', 'm')
