from selenium import webdriver as www
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as NSE

from twilio.rest import Client
from datetime import datetime, timedelta, timezone
from time import sleep, time, mktime
from os import getenv
from os.path import exists
from dotenv import load_dotenv
from pathlib import Path  # python3 only

import sys
import logging

logging.basicConfig(filename='meh.log',level=logging.INFO)

env_path = Path('.') / '.env'

if not exists(env_path):
    print('Error: .env file not found')
    exit(1)

load_dotenv(dotenv_path=env_path)

# home page
FLIPPER_SELECTOR = 'div[class="flipper"] button'
FLIPPED_SELECTOR = 'div[class="meh-button flip-container flip"]'
PRODUCT_SPEC_SELECTOR = 'section[class="features"] ul li'
PRODUCT_TITLE_SELECTOR = 'section[class="features"] h2'
PRODUCT_PHOTO_ID = 'gallery-photo-1'

# signin page
SIGNIN = 'https://meh.com/account/signin'
SIGNIN_USER_ID = 'user'
SIGNIN_PASS_ID = 'password'
SIGNIN_BUTTON_SELECTOR = 'button[class="primary"]'


def send_product_info(sms_body, img):
    '''Send pics'''
    # twilio credentials
    ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
    AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
    TO_NUMBER = getenv('TWILIO_TO_NUMBER')
    FROM_NUMBER = getenv('TWILIO_FROM_NUMBER')

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        to=TO_NUMBER,
        from_=FROM_NUMBER,
        body=sms_body,
        media_url=img
    )

def meh_function():
    '''Does what project is supposed to achieve'''
    try:
        # set up cursor
        options = Options()
        options.set_headless(True)
        # options.set_headless(False) # for debugging

        choices = ['chromium-browser', 'google-chrome', 'firefox']
        browser_choice = getenv('BROWSER_CHOICE')
        if browser_choice not in choices:
            browser = www.Firefox(firefox_options=options, executable_path='./geckodriver')
        elif browser_choice.lower() == choices[2]:
            browser = www.Firefox(firefox_options=options, executable_path='./geckodriver')
        elif browser_choice.lower() in choices[:2]:
            options.binary_location = '/usr/bin/' + browser_choice
            browser = www.Chrome(chrome_options=options, executable_path='./chromedriver')

        # driver wait
        wait = WebDriverWait(browser, 10)  # maximum wait time

        # First sign in
        browser.get(SIGNIN)

        signin_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, SIGNIN_BUTTON_SELECTOR)
        ))
        signin_input_user = browser.find_element_by_id(SIGNIN_USER_ID)
        signin_input_pass = browser.find_element_by_id(SIGNIN_PASS_ID)

        print('Signing in...')
        logging.info('Signing in...')
        signin_input_user.clear()
        signin_input_pass.clear()
        signin_input_user.send_keys(getenv('MEH_USER'))
        signin_input_pass.send_keys(getenv('MEH_PASS'))
        signin_button.click()

        # the meh icon, they call it a flipper
        flipper = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, FLIPPER_SELECTOR)
        ))

        browser.find_element_by_css_selector(FLIPPED_SELECTOR)
        print('Icon already flipped')
        logging.info('Icon already flipped')
    except NSE as nse:
        print('Flipping the flipper')
        logging.info('Flipping the flipper')
        flipper.click()
    except KeyboardInterrupt:
        print('\n')
        logging.info('KeyboardInterrupt')
        browser.quit()
        exit(0)
    except Exception as e:
        print('\n')
        logging.error(e)
        browser.quit()
        exit(1337)
    finally: # optional text alert
        SEND_SMS = getenv('SEND_SMS')
        if SEND_SMS:
            print('Texting product...')
            logging.info('Texting product...')
            # construct message body
            sms_body = 'Meh:\n'
            sms_body += browser.find_element_by_css_selector(PRODUCT_TITLE_SELECTOR).text
            img = browser.find_element_by_id(PRODUCT_PHOTO_ID).get_attribute('src')
            send_product_info(sms_body, img)
        browser.quit()

def seconds_till_tomorrow():
    n = datetime.utcnow() - timedelta(hours=4)
    return (23 - n.hour) * 3600 + (59 - n.minute) * 60 + (60 - n.second), n

def countdown():
    sec = seconds_till_tomorrow()
    p = '{} - {:05d} seconds left till tomorrow...'.format(sec[1], sec[0])
    print(p, end='\r', flush=True)
    sleep(1)
    while sec[0] > 0:
        sec = seconds_till_tomorrow()
        p = '{} - {:05d} seconds left till tomorrow...'.format(sec[1], sec[0])
        print(p, end='\r', flush=True)
        sleep(1)
    print('\n')


if __name__ == '__main__':
    if getenv('RUN_IT_ONCE'):
        print('Run it once')
        logging.info('Run it once')
        meh_function()
    elif not getenv('DO_THIS_EVERY_DAY'):
        print('Run it only once')
        logging.info('Run it only once')
        meh_function()
        exit(0)

    while True:
        try:
            countdown()
            sleep(5)
        except Exception as e:
            print(e)
            exit(2)
        sleep(20)
        meh_function()
