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

import sys
import logging

# load ".env" file
load_dotenv(dotenv_path='.env')

# logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('meh.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# home page
FLIPPER_SELECTOR = 'div[class="flipper"] button'
FLIPPED_SELECTOR = 'div[class="meh-button flip-container flip"]'
PRODUCT_SPEC_SELECTOR = 'section[class="features"] ul li'
PRODUCT_TITLE_SELECTOR = 'section[class="features"] h2'
PRODUCT_PHOTO_ID = 'gallery-photo-1'

# Meh elements/URLs
HOMEPAGE = 'https://meh.com/'
SIGNIN = 'https://meh.com/account/signin'
SIGNIN_USER_ID = 'user'
SIGNIN_PASS_ID = 'password'
SIGNIN_BUTTON_SELECTOR = 'button[class="primary"]'


class Meh:
    def __init__(self, browser):
        self.browser = browser
        self.logged_in = False

    def text(self):
        '''Send pics and title'''
        browser = self.browser

        SEND_SMS = getenv('SEND_SMS')
        if not SEND_SMS:
            logging.info('Texting not configured')
            return

        logging.info('Texting product...')

        # construct message body
        sms_body = 'Meh:\n'
        sms_body += self.browser.find_element_by_css_selector(PRODUCT_TITLE_SELECTOR).text
        img = self.browser.find_element_by_id(PRODUCT_PHOTO_ID).get_attribute('src')

        # twilio credentials
        ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
        AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
        TO_NUMBER = getenv('TWILIO_TO_NUMBER')
        FROM_NUMBER = getenv('TWILIO_FROM_NUMBER')

        # Texting
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            body=sms_body,
            media_url=img
        )


    def login(self):
        '''Log into Meh'''
        # First sign in
        self.browser.get(SIGNIN)

        signin_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, SIGNIN_BUTTON_SELECTOR)
        ))

        signin_input_user = self.browser.find_element_by_id(SIGNIN_USER_ID)
        signin_input_pass = self.browser.find_element_by_id(SIGNIN_PASS_ID)

        signin_input_user.clear()
        signin_input_pass.clear()
        signin_input_user.send_keys(getenv('MEH_USER'))
        signin_input_pass.send_keys(getenv('MEH_PASS'))

        m = 'Signing in...'
        logger.info(m)
        signin_button.click()
        sleep(3) # give it 3 seconds to authenticate
        if SIGNIN not in self.browser.current_url:
            self.logged_in = True

    def flip(self):
        '''Does what project is supposed to achieve'''
        flipped = True
        message = 'Icon already flipped'

        if self.logged_in:
            try:
                # the meh icon, they call it a flipper
                flipper = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, FLIPPER_SELECTOR)
                ))
                self.browser.find_element_by_css_selector(FLIPPED_SELECTOR)
            except NSE as nse:
                flipped = False
                message = 'Flipping the flipper'
            except Exception as e:
                logger.error(e)
                self.browser.quit()
                raise
            finally:
                print(message)
                logger.info(message)
                if flipped:
                    flipper.click()
        else:
            m = 'You\'re not logged in'
            print(m)
            logger.error(m)

    def homepage(self):
        '''Goes to the home page of Meh, and optionally texts item'''

        logger.info('Visiting homepage...')

        try:
            self.browser.get(HOMEPAGE)
            self.text()
        except Exception as e:
            logger.error(e)
            self.browser.quit()
            raise

    def midnight_fun(self):
        '''Do the whole thing'''
        self.homepage()
        self.login()
        self.flip()

def seconds_till_tomorrow():
    global asdf
    n = datetime.utcnow() - timedelta(hours=4)
    return (23 - n.hour) * 3600 + (59 - n.minute) * 60 + (60 - n.second), n

def countdown():
    sec = seconds_till_tomorrow()
    f = '{} - {:05d} seconds left till tomorrow...'
    p = f.format(sec[1], sec[0])
    print(p, end='\r', flush=True)
    sleep(1)
    while sec[0] > 0:
        sec = seconds_till_tomorrow()
        p = f.format(sec[1], sec[0])
        print(p, end='\r', flush=True)
        sleep(1)
    print()

if __name__ == '__main__':
    if not exists('.env'):
        logger.info('You don\'t have a .env file')
        exit(1)

    # browser initialization
    options = Options()
    options.set_headless(True)

    choices = ['chromium-browser', 'google-chrome', 'firefox']
    browser_choice = getenv('BROWSER_CHOICE')
    if browser_choice not in choices:
        browser = www.Firefox(
            firefox_options=options, 
            executable_path='./geckodriver'
        )
    elif browser_choice.lower() == choices[2]:
        browser = www.Firefox(
            firefox_options=options,
            executable_path='./geckodriver'
        )
    elif browser_choice.lower() in choices[:2]:
        options.binary_location = '/usr/bin/' + browser_choice
        browser = www.Chrome(
            chrome_options=options, 
            executable_path='./chromedriver'
        )
    else:
        logger.error('Shit happens. Browser startup failure')
        exit(1) # shit happens

    # driver wait
    wait = WebDriverWait(browser, 10)  # maximum wait time

    # Meh wrapper
    meh = Meh(browser)

    if getenv('RUN_IT_ONCE'):
        logger.info('Run it once')
        meh.midnight_fun()
    elif not getenv('DO_THIS_EVERY_DAY'):
        logger.info('Run it only once')
        meh.midnight_fun()
        exit(0)

    while True:
        countdown()
        logger.info('Countdown is over. Wait 30 seconds...')
        # sleep(30) # to avoid high traffic
        meh.midnight_fun()
