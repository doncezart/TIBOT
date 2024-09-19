import os
import pyfiglet
import webbrowser
from time import sleep
from os import system, name
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--mute-audio")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

client_version = "1.2.1"


def beautify(arg):
    return format(arg, ',d').replace(',', '.')

system(f'title TIBOT {client_version}')

def viewbot():
    captcha = False
    views_count = 0
    cycle_count = 0
    total_views = 0
    new_views = 0
    VIDEO_URL = input("[>] TikTok video URL: ")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 800)
    driver.get('https://vipto.de/')
    print('[!] Solve the captcha')
    captcha = True

    while captcha:
        # Waits for the captcha to be completed and attempts to find the proper button.
        try:
            driver.find_element(By.XPATH,'/html/body/div[6]/div/div[2]/div/div/div[6]/div/button').click()
        except (common.exceptions.NoSuchElementException, common.exceptions.ElementClickInterceptedException):
            continue
        driver.set_window_position(-10000, 0)
        print('[!] TIBOT is running')
        captcha = False

    # Pastes the URL into the "Enter video URL" textbox.
    try:
        driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/input').send_keys(VIDEO_URL)
    except (common.exceptions.ElementNotInteractableException):
        print('[!] Followbot is not available at the moment, try something else')
        driver.quit()
        runbot()

    while True:
        # Clicks the "Search" button.
        driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button').click()
        sleep(3)
        if views_count>0:
            try:
                print('[!] Cycle completed, generating metrics')
                new_views = views_count
                views_count = driver.find_element(By.XPATH,'/html/body/div[10]/div/div/div[1]/div/form/button').text
                views_count = int(views_count.replace(',',''))
                new_views = views_count - new_views
                total_views = total_views + new_views
                print(f'[!] Views counter: {views_count:,} (+{new_views:,} new views, total: +{total_views:,})')
            except:
                print('[!] Unrecognized error, retrying')
                continue
            
        else:
            try:
                views_count = driver.find_element(By.XPATH,'/html/body/div[10]/div/div/div[1]/div/form/button').text
                views_count = int(views_count.replace(',',''))
                print(f'[!] Views counter: {views_count:,}')
            except common.exceptions.NoSuchElementException:
                try:
                    if driver.find_element(By.XPATH,'/html/body/div[4]/div[5]/div/div/span').text:
                        driver.quit()
                        print(f'\n[!] Invalid URL, please try again')
                        viewbot()
                        break
                except common.exceptions.NoSuchElementException:
                    try:
                        print('[!] Cooldown is still active')
                        thedelay = driver.find_element(By.XPATH,'/html/body/div[10]/div/div/span[1]').text
                        minutes = int(thedelay[12:-43])
                        seconds = int(thedelay[24:-30])
                        cooldown = minutes* 60 + seconds
                        thedelay = str(thedelay[:-22])
                        print('[!] '+thedelay+' for the next cycle')
                    except ValueError:
                        print('[!] Unrecognized error, retrying')
                        continue
                    
                    while cooldown > 0:
                        cooldown -= 1
                        os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Boosted: +{total_views:,} ^| Cycles: {cycle_count} ^| Please wait 'f'{cooldown}seconds')
                        sleep(1)
                    os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Boosted: +{total_views:,} ^| Cycles: {cycle_count} ^| Starting a new cycle')
                    continue

        try:
            # Clicks the "Send Views" button.
            sleep(2)
            driver.find_element(By.XPATH,'/html/body/div[10]/div/div/div[1]/div/form/button').send_keys(Keys.TAB)
            driver.find_element(By.XPATH,'/html/body/div[10]/div/div/div[1]/div/form/button').send_keys(Keys.ENTER)
            sleep(2)
        except common.exceptions.NoSuchElementException:
            driver.quit()
            print(f'\n[!] Invalid URL, please try again')
            viewbot()
            break
        else:
            try:
                print(f'\n[+] New views cycle submitted')
                cycle_count += 1
                os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Total boosted: +{total_views:,} ^| Cycles: {cycle_count}')
                sleep(5)
                thedelay = driver.find_element(By.XPATH,'/html/body/div[10]/div/div/span[1]').text
                minutes = int(thedelay[12:-43])
                seconds = int(thedelay[24:-30])
                cooldown = minutes* 60 + seconds
                thedelay = str(thedelay[:-22])
                print('[!] '+thedelay+' for the next cycle')
            except ValueError:
                print('[!] Unrecognized error, retrying')
                continue

            while cooldown > 0:
                cooldown -= 1
                os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Boosted: +{total_views:,} ^| Cycles: {cycle_count} ^| Please wait 'f' {cooldown} seconds')
                sleep(1)
            os.system(f'title [TIBOT] - Views Count: {beautify(views_count)} ^| Boosted: +{total_views:,} ^| Cycles: {cycle_count} ^| Starting a new cycle')

def runbot():
    CHOICE = int(input("[>] Select choice: "))

    if CHOICE == 1:
        viewbot()

    if CHOICE == 2 or CHOICE == 3 or CHOICE == 4 or CHOICE == 5:
        print('\n[!] Currently unavailable, please check for updates or try again')
        UPDATE = input("[>] Would you like to check for updates? Y/N: ")
        if UPDATE == "Y":
            webbrowser.open('https://github.com/goldieczr/TIBOT/releases', new=0, autoraise=True)
            print(f'[!] URL opened, current version: v{client_version}\n')
            runbot()
        if UPDATE == "N":
            print('')
            runbot()
        else:
            print("[!] Invalid choice, returning to menu")
            runbot()

    else:
        print('\n[!] Incorrect choice, please try again')
        runbot()

print(pyfiglet.figlet_format(f"TIBOT {client_version}", font="slant"))
print("[1]. Views\n[2]. Likes | UNAVAILABLE\n[3]. Shares | UNAVAILABLE\n[4]. Followers | UNAVAILABLE\n[5]. Comment Likes | UNAVAILABLE\n[6]. Livestream [VS+ Likes] | UNAVAILABLE\n")
runbot()
