import os
import time
import pyfiglet
import threading
from time import sleep
from os import system, name
from selenium import webdriver, common
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

def beautify(arg):
    return format(arg, ',d').replace(',', '.')


system('title TIBOT 1.0')
captcha = False
views_sent = 0

print(pyfiglet.figlet_format("TIBOT 1.0", font="slant"))
print("[1]. Views\n[2]. Likes | UNAVAILABLE\n[3]. Shares | UNAVAILABLE\n[4]. Followers | UNAVAILABLE\n[5]. Comment Likes | UNAVAILABLE\n[6]. Livestream [VS+ Likes] | UNAVAILABLE\n")
CHOICE = int(input("[>] Select choice: "))

if CHOICE == 1:
    VIDEO_URL = input("[>] TikTok video URL: ")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 800)
    driver.get('https://vipto.de/')
    print('[!] Solve the captcha')
    captcha = True

    while captcha:
        # Attempts to select the "Views" option.
        try:
            driver.find_element(By.XPATH, 
                '/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button'
            ).click()
        except (
            common.exceptions.NoSuchElementException,
            common.exceptions.ElementClickInterceptedException
        ):
            continue
        driver.set_window_position(-10000, 0)
        print('[!] TIBOT is running')
        captcha = False

    # Pastes the URL into the "Enter video URL" textbox.
    driver.find_element(By.XPATH, 
        '/html/body/div[4]/div[5]/div/form/div/input'
    ).send_keys(VIDEO_URL)

    while True:
        # Clicks the "Search" button.
        driver.find_element(By.XPATH, '/html/body/div[4]/div[5]/div/form/div/div/button').click()
        sleep(2)

        try:
            # Clicks the "Send Views" button.
            driver.find_element(By.XPATH, 
                '/html/body/div[4]/div[5]/div/div/div[1]/div/form/button'
            ).click()
            print('[+] Sending views')
        except common.exceptions.NoSuchElementException:
            driver.quit()
            print(
                f'\n[!] Invalid URL'
            )
            print('TIBOT will exit in 5 seconds')
            sleep(5)
            exit(0)
            break
        else:
            views_sent += 1000
            print(f'[+] 1000 views sent. Total views: {beautify(views_sent)}')
            os.system(f'title [TIBOT] - Views Sent: {beautify(views_sent)}')

            seconds = 180
            while seconds > 0:
                seconds -= 1
                os.system(
                    f'title [TIBOT] - Views Sent: {beautify(views_sent)} ^| Sending '
                    f'in: {seconds} seconds'
                )
                sleep(1)
            os.system(
                f'title [TIBOT] - Views Sent: {beautify(views_sent)} ^| Sending...'
            )

if CHOICE == 2 or CHOICE == 3 or CHOICE == 4 or CHOICE == 5:
    print('\n[!] Currently unavailable, please check for updates')
    print('TIBOT will exit in 5 seconds')
    sleep(5)
    exit(0)

else:
    print('\n[!] Incorrect choice')
    print('TIBOT will exit in 5 seconds')
    sleep(5)
    exit(0)
