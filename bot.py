import logging
import sys
from datetime import datetime, timedelta, timezone
from os import getenv
from os.path import exists
from time import mktime, sleep, time

from dotenv import load_dotenv
from selenium import webdriver as www
from selenium.common.exceptions import ElementNotInteractableException as ENI
from selenium.common.exceptions import NoSuchElementException as NSE
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twilio.rest import Client

# load ".env" file
load_dotenv(dotenv_path='.env')


class Meh:
    '''Everything you need in for clicking'''
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

    def __init__(self):
        # self.logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create handlers
        file_handler = logging.FileHandler('meh.log')
        file_handler.setLevel(logging.INFO)

        # custom timezone
        def converter(x, y):
            return (datetime.utcnow() - timedelta(hours=4)).timetuple()

        logging.Formatter.converter = converter

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        )
        file_handler.setFormatter(formatter)

        # add the handlers to the self.logger
        self.logger.addHandler(file_handler)

        if not exists('.env'):
            print('You don\'t have a .env file')
            self.logger.info('You don\'t have a .env file')
            exit(1)

        # browser initialization
        options = Options()
        options.set_headless(True)
        choices = ['chromium-browser', 'google-chrome', 'firefox']
        browser_choice = getenv('BROWSER_CHOICE')
        if browser_choice not in choices:
            self.browser = www.Firefox(
                firefox_options=options,
                executable_path='./geckodriver'
            )
        elif browser_choice.lower() == choices[2]:
            self.browser = www.Firefox(
                firefox_options=options,
                executable_path='./geckodriver'
            )
        elif browser_choice.lower() in choices[:2]:
            options.binary_location = '/usr/bin/' + browser_choice
            self.browser = www.Chrome(
                chrome_options=options,
                executable_path='./chromedriver'
            )
        else:
            self.logger.error('Browser startup failure')
            exit(1)  # shit happens

        # driver wait
        self.wait = WebDriverWait(self.browser, 300)  # maximum wait time
        self.logged_in = False

    def text_product(self):
        '''Send pics and title'''
        SEND_SMS = getenv('SEND_SMS')
        if not SEND_SMS:
            self.logger.info('Texting not configured')
            return 1

        # construct message body
        sms_body = 'Meh:\n'
        sms_body += self.browser.find_element_by_css_selector(
            self.PRODUCT_TITLE_SELECTOR).text
        img = self.browser.find_element_by_id(
            self.PRODUCT_PHOTO_ID).get_attribute('src')

        # twilio credentials
        ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
        AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
        TO_NUMBER = getenv('TWILIO_TO_NUMBER')
        FROM_NUMBER = getenv('TWILIO_FROM_NUMBER')

        # Texting
        self.logger.info('Texting product...')
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            body=sms_body,
            media_url=img
        )

        return 0

    def text_error(self, e):
        '''Send error'''
        SEND_SMS = getenv('SEND_SMS')
        if not SEND_SMS:
            self.logger.info('Texting not configured')
            return 1

        # construct message body
        sms_body = 'ERROR: {}'.format(e)

        # twilio credentials
        ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
        AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
        TO_NUMBER = getenv('TWILIO_TO_NUMBER')
        FROM_NUMBER = getenv('TWILIO_FROM_NUMBER')

        # Texting
        self.logger.info('Texting error...')
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            body=sms_body
        )

        return 0

    def login(self):
        '''Log into Meh'''
        # First sign in
        self.browser.get(self.SIGNIN)

        signin_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.SIGNIN_BUTTON_SELECTOR)
        ))

        signin_input_user = self.browser.find_element_by_id(
            self.SIGNIN_USER_ID)
        signin_input_pass = self.browser.find_element_by_id(
            self.SIGNIN_PASS_ID)

        signin_input_user.clear()
        signin_input_pass.clear()
        signin_input_user.send_keys(getenv('MEH_USER'))
        signin_input_pass.send_keys(getenv('MEH_PASS'))

        self.logger.info('Signing in...')
        signin_button.click()
        sleep(3)  # give it 3 seconds to authenticate
        if self.SIGNIN not in self.browser.current_url:
            self.logged_in = True

    def flip(self):
        '''Does what project is supposed to achieve'''
        if not self.logged_in:
            self.logger.error('You\'re not logged in')
            return 1

        # the meh icon, they call it a flipper
        self.logger.info('Flipping the flipper...')
        try:
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.FLIPPER_SELECTOR)
            )).click()
            sleep(1)
            self.logger.info('Done')
        except ENI as eni:
            self.logger.info('Flipper is already flipped')
        except Exception as e:
            self.logger.error(e)
            self.browser.quit()
            self.text_error(e)
            raise
        finally:
            return 0

    def homepage(self):
        '''Goes to the home page of Meh, and optionally texts item'''
        self.logger.info('Visiting homepage...')
        try:
            self.browser.get(self.HOMEPAGE)
            self.text_product()
        except Exception as e:
            self.logger.error(e)
            self.browser.quit()
            self.text_error(e)
            raise

    def midnight_fun(self):
        '''Do the whole thing'''
        self.homepage()
        self.login()
        self.flip()

    def customTime(*args):
        utc_dt = utc.localize(datetime.utcnow())
        my_tz = timezone("US/Eastern")
        converted = utc_dt.astimezone(my_tz)
        return converted.timetuple()


def dst():
    ''' I don't trust the Python's native check '''
    ''' Returns the hour difference between EST and UTC '''

    n = datetime.utcnow()
    month = n.month

    if month < 3 or month > 11:
        return 5
    if month > 3 and month < 11:
        return 4

    day_of_week = n.weekday() + 1  # monday is 0
    last_sunday = n.day - day_of_week

    # In march, we are DST if our previous sunday was on or after the 8th.
    if month == 3:
        return 4 if last_sunday >= 8 else 5

    # In november we must be before the first sunday to be dst.
    # That means the previous sunday must be before the 1st.
    return 4 if last_sunday <= 0 else 5


def seconds_till_tomorrow():
    '''Count the seconds until midnight'''
    n = datetime.utcnow() - timedelta(hours=dst())
    return (23 - n.hour) * 3600 + (59 - n.minute) * 60 + (60 - n.second), n


def countdown():
    '''Count down until midnight'''
    sec = seconds_till_tomorrow()
    f = '{} - {:05d} seconds left till tomorrow...'
    p = f.format(sec[1], sec[0])
    print(p, end='\r', flush=True)
    sleep(1)
    while sec[0] > 1:
        sec = seconds_till_tomorrow()
        p = f.format(sec[1], sec[0])
        print(p, end='\r', flush=True)
        sleep(1)
    print()


if __name__ == '__main__':
    # wait time
    wait_time = 30

    # Meh wrapper
    meh = Meh()

    # initial behavior
    if getenv('RUN_IT_ONCE'):
        meh.logger.info('Run it once')
        meh.midnight_fun()
    elif not getenv('DO_THIS_EVERY_DAY'):
        meh.logger.info('Run it only once')
        meh.midnight_fun()
        exit(0)

    while True:
        countdown()
        meh.logger.info(
            'Countdown is over. Wait {} seconds...'.format(wait_time))
        meh.midnight_fun()
