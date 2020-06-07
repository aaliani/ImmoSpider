from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from datetime import datetime, timedelta
import subprocess
import time
import pandas as pd
import numpy as np

import configparser

def get_name(driver):
    
    h4 = driver.find_elements_by_css_selector('h4')

    for h in h4:
        t = h.get_attribute('innerHTML').strip()
        if t.startswith('Kontaktanfrage'):
            name = t.replace('Kontaktanfrage an ', '')
    
    return name


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
# CHROMEDRIVER_PATH = '/Applications/chromedriver'

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")

# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

contact_area = driver.find_element_by_class_name('is24-contact-bar-area')
agent_name = driver.find_element_by_css_selector('.style__realtorInfoNameAndRatingContainer___327eu div').get_attribute('innerHTML')
contact_btn = contact_area.find_element_by_class_name('button-primary')

contact_postfix = '#/basicContact/email'

name = get_name(driver)

msg = """Hallo %s,

Ich habe große Interesse an diesem Objekt.

Ich habe gerade nach Berlin umgezogen, um meine neue Arbeit zu anfangen. Ich Arbeite als Solutions Engineer im IT Bereich. Ich suche jetzt eine langfristige Wohnung. Dieses Objekt hat insbesondere mein Interesse geweckt.

Ich verdiene Brutto 3500 € Gehalt pro Monat mit meiner neuen Arbeit. Alle Unterlagen können sie auf diesem Link finden:
https://drive.google.com/file/d/1-rjEFWsQZ6tE2Jt5QhyX16_nBxPHSkqe/view

Also, wenn verfügbar, bitte mir rückmelden. Ich habe große Interesse! 

Ich freue mich auf Ihre Rückmeldung.

Viele Grüße
Aqeel""" % name

msg_field = {'id': 'contactForm-Message', 'val': msg}
salutation = {'id': 'contactForm-salutation', 'val': 'MALE'}
firstname = {'id': 'contactForm-firstName', 'val': 'Aqeel'}
lastname = {'id': 'contactForm-lastName', 'val': 'Aliani'}
email = {'id': 'contactForm-emailAddress', 'val': 'aqeel.aliani@gmail.com'}
phone = {'id': 'contactForm-phoneNumber', 'val': '17681000781'}
street = {'id': 'contactForm-street', 'val': 'Heinrich-Heine-Str'}
house_no = {'id': 'contactForm-houseNumber', 'val': '24'}
plz = {'id': 'contactForm-postcode', 'val': '10179'}
city = {'id': 'contactForm-city', 'val': 'Berlin'}

move_in = {'id' : 'contactForm-moveInDateType', 'val': 'FLEXIBLE'}
pets = {'id' : 'contactForm-petsInHousehold', 'val': 'Keine'}
employment = {'id' : 'contactForm-employmentRelationship', 'val': 'WORKER'}
income = {'id' : 'contactForm-income', 'val': 'OVER_2000_UPTO_3000'}
documents = {'id' : 'contactForm-applicationPackageCompleted', 'val': 'true'}

policycheck_class = 'label-checkbox'
submit_btn_css = '.contentContainer button.button-primary'

fields = [msg_field, firstname, lastname, email, phone, street, house_no, plz, city]

for
    driver.get(link + contact_postfix)

    for field in fields:
        driver.find_element_by_id(field['id']).send_keys(field['val'])

    Select(driver.find_element_by_id(salutation['id'])).select_by_value(salutation['val'])

    driver.find_element_by_css_selector(submit_btn_css).click()
    e = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, submit_btn_css)))

    driver.find_element_by_id(pets['id']).send_keys(pets['val'])
    driver.find_element_by_class_name(policycheck_class).click()

    for field in [move_in, employment, income, documents]:
        Select(driver.find_element_by_id(field['id'])).select_by_value(field['val'])

# driver.close


        