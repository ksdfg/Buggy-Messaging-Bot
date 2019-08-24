import pyautogui as py
import pandas as pd
import time

whatsapp_api = "https://api.whatsapp.com/send?phone=91"
hello = "Hey, "
message = "This is to remind you that the C/C++ workshop is tomorrow at 3:30pm. Location will be given out soon (Most probably SL 2,3 Lab in N-building, 1st floor). Do confirm if you'll be attending the workshop :D\n\nSee you tomorrow!"

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
    py.typewrite(api, interval = 0.01)
    py.press('enter')
    time.sleep(3)
    py.click(680, 360)
    time.sleep(15)
    py.typewrite(final, interval = 0.01)
    py.press('enter')
    time.sleep(5)
    py.hotkey('ctrl', 'w')
             

if __name__ == "__main__":
    timer()
    excel = pd.read_excel("New.xlsx")
    numbers = excel['Number'].tolist()
    names = excel['Name'].tolist()
    ctr = 0
    for num, name in zip(numbers, names):
        sendMessage(num, name)
        ctr += 1
        if ctr == 30:
            break

    py.hotkey('win', 'm')
    
