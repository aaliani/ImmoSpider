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

config = configparser.ConfigParser()
inifile = 'config.ini'
config.read(inifile)
format = "%Y-%m-%dT%H:%M:%S"

for i in range(5):
    t = datetime.now().strftime(format)
    # bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    bashCommand = "echo '%s'" % t
    bashCommand = "ls"
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()
    # print(process.communicate())
    print(config['global']['last_queried'])
    config['global']['last_queried'] = t
    time.sleep(1)

with open(inifile, 'w') as configfile:
    config.write(configfile)

t = (datetime.now() - timedelta(hours = 13)).strftime("%Y-%m-%dT%H:%M:%S")

urlbase = 'https://www.immobilienscout24.de/Suche/shape/wohnung-mieten'

shape_id = 'e3BsX0l1ZGBwQWpvQG9NZ0RrdUFoeUB8TH5Ab1tgbUBjdEBsTGVzQWFFY1B6TGdJbE1nUnxKYUNqSGJFckJsRGxNbk5wQ2NQekZfXGpMeVl7QnNHeUd5S2tSfVN9UW9rQGtGZXVAUHdAcFNteUB8Q3twQHBDb3BBeUppb0BnQGdfQHBRbUZwQXdNcEF9eEBoQmtwQGpNb1ViSHVQcFV1ZkB8U2NPaE99YkByQnNPcEF7SmhGYURwV3xFYkpjQXpoQGpaeFl7Un5OdVd2SnNXeEp9eEB9QnNHU3lZc1VzVndacUd7R2NBeUdmQ3NCfExtakBwYUFfVHhHZWpAZlB5SXFrQGdnQHZYZ1RiSGFHfUZ_T3NRa01xa0BfTm9Val5jfEByUWtfQWRFYVV5TmNjQHFOcWBAdV5oYUBxVHpLe1Z_VGNJYEB1TWNIb1N0R2tBeUNhTGZKZ1RySG9VcGtAX2JAamtAfVB7Y0B3SmNed0txXWVVZ1hjSX1Ua05nSX1RP29GYGRAcUJydEBHck13WGFDa2pBYkF9UnhKZUV2WHJAYnNAY0FadU5sW2tMck9xd0BsaEF9U2JoQXdDclFxTnx0QGhDaHBAWnJhQFV6YUByQXBsQGNBdFhpT3pJfkZ6TGxEcEdoQn5GdkJsTW1KcE5lQ2haZ0Z4WHlFektnQm5GZ0JoaEB9QG5rQHBBYlZqTXppQGpLcFVxYUBkckFSblZqXXxEYnRAdXVAelJpW3pKd0xwRm9NalliXmJLfExiZ0B2UXBRbltoR3JQX0R6bEBoQWRQelt8VUFSfUxge0F7SX5vQElod0B8QWRJblZuY0BwYkFlSX5dbkY.'

params = ['haspromotion=false',
'numberofrooms=2.0-',
'price=-500.0',
'livingspace=50.0-',
'lastmodification=%s'%t,
'sorting=2',
'enteredFrom=result_list#']

main_url = "%s?shape=%s&%s"%(urlbase,shape_id,"&".join(params))

driver.get(url)
ads = driver.find_elements_by_class_name('result-list__listing')

links = []

for ad in ads:
    try:
        links.append(ad.find_element_by_tag_name('a').get_attribute('href'))
    except: continue

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


        