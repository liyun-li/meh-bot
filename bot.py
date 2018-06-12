from selenium import webdriver as www
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as NSE

from twilio.rest import Client

from time import sleep
from os import getenv
from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# set up cursor
options = Options()
options.set_headless(True)

options.set_headless(False) # for debugging
browser = www.Firefox(firefox_options=options, executable_path='./geckodriver')

# driver wait
wait = WebDriverWait(browser, 10)  # maximum wait time

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

# twilio stuff
ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
TO_NUMBER = getenv('TWILIO_TO_NUMBER')
FROM_NUMBER = getenv('TWILIO_FROM_NUMBER')

def send_product_info(browser):
    sms_body = 'Meh:\n'
    sms_body += browser.find_element_by_css_selector(PRODUCT_TITLE_SELECTOR).text
    img = browser.find_element_by_id(PRODUCT_PHOTO_ID).get_attribute('src') # 1 photo
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        to=TO_NUMBER,
        from_=FROM_NUMBER,
        body=sms_body,
        media_url=img
    )

if __name__ == '__main__':
    browser.get(SIGNIN)

    signin_button = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, SIGNIN_BUTTON_SELECTOR)
    ))
    signin_input_user = browser.find_element_by_id(SIGNIN_USER_ID)
    signin_input_pass = browser.find_element_by_id(SIGNIN_PASS_ID)

    print('Signing in...')
    signin_input_user.clear()
    signin_input_pass.clear()
    signin_input_user.send_keys(getenv('MEH_USER'))
    signin_input_pass.send_keys(getenv('MEH_PASS'))
    signin_button.click()

    flipper = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, FLIPPER_SELECTOR)
    ))

    try:
        browser.find_element_by_css_selector(FLIPPED_SELECTOR)
        print('Icon already flipped')
    except:
        print('Flipping the flipper')
        flipper.click()
    finally:
        print('Texting product...')
        send_product_info(browser)
    
    sleep(3)
    print('Done. Bye')
    browser.quit()
