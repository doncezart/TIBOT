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

system('title TIBOT 1.1')

def startbot():
    captcha = False
    views_count = 0
    VIDEO_URL = input("[>] TikTok video URL: ")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 800)
    driver.get('https://vipto.de/')
    print('[!] Solve the captcha')
    captcha = True

    while captcha:
        # Attempts to select the "Views" option.
        try:
            driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button').click()
        except (
            common.exceptions.NoSuchElementException,
            common.exceptions.ElementClickInterceptedException
        ):
            continue
        driver.set_window_position(-10000, 0)
        print('[!] TIBOT is running')
        captcha = False

    # Pastes the URL into the "Enter video URL" textbox.
    driver.find_element(By.XPATH,'/html/body/div[4]/div[5]/div/form/div/input').send_keys(VIDEO_URL)

    while True:
        # Clicks the "Search" button.
        driver.find_element(By.XPATH, '/html/body/div[4]/div[5]/div/form/div/div/button').click()
        sleep(2)
        if views_count>0:
            print('[!] Cycle completed, generating metrics')
            new_views = views_count
            views_count = driver.find_element(By.XPATH,'/html/body/div[4]/div[5]/div/div/div[1]/div/form/button').text
            views_count = int(views_count.replace(',',''))
            new_views = views_count - new_views
            print(f'[!] Views counter: {views_count:,} (+{new_views:,})')
        else:
            views_count = driver.find_element(By.XPATH,'/html/body/div[4]/div[5]/div/div/div[1]/div/form/button').text
            views_count = int(views_count.replace(',',''))
            print(f'[!] Views counter: {views_count:,}')
        try:
            # Clicks the "Send Views" button.
            driver.find_element(By.XPATH, '/html/body/div[4]/div[5]/div/div/div[1]/div/form/button').click()
        except common.exceptions.NoSuchElementException:
            driver.quit()
            print(f'\n[!] Invalid URL, please try again')
            startbot()
            break
        else:
            print(f'[+] New views cycle submitted')
            os.system(f'title [TIBOT] - Views Count: {beautify(views_count)}')

            sleep(5)
            thedelay = driver.find_element(By.XPATH,'/html/body/div[4]/div[5]/div/div/h4').text
            minutes = int(thedelay[12:-43])
            seconds = int(thedelay[24:-30])
            cooldown = minutes* 60 + seconds
            thedelay = str(thedelay[:-22])
            print('[!] '+thedelay+' for the next cycle')
            
            while cooldown > 0:
                cooldown -= 1
                os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Sending 'f'in: {cooldown} seconds')
                sleep(1)
            os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Sending...')
def runbot():
    CHOICE = int(input("[>] Select choice: "))

    if CHOICE == 1:
        startbot()

    if CHOICE == 2 or CHOICE == 3 or CHOICE == 4 or CHOICE == 5:
        print('\n[!] Currently unavailable, please check for updates or try again')
        runbot()

    else:
        print('\n[!] Incorrect choice, please try again')
        runbot()

print(pyfiglet.figlet_format("TIBOT 1.1", font="slant"))
print("[1]. Views\n[2]. Likes | UNAVAILABLE\n[3]. Shares | UNAVAILABLE\n[4]. Followers | UNAVAILABLE\n[5]. Comment Likes | UNAVAILABLE\n[6]. Livestream [VS+ Likes] | UNAVAILABLE\n")
runbot()
