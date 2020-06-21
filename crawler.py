from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime, timedelta
from dateutil.parser import parse
import subprocess
import time
import pandas as pd
import numpy as np

import sys
import re
import ast
import stringcase

class Crawler():

    def __init__(self):

        CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
        # CHROMEDRIVER_PATH = '‪D:\Dev\chromedriver.exe'
        # CHROMEDRIVER_PATH = '/Applications/chromedriver'

        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")

        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

        self.possible_tags = ['Garten/ -mitbenutzung',
                                'Gäste-WC',
                                'WG-geeignet',
                                'Keller',
                                'Balkon/ Terrasse',
                                'Personenaufzug',
                                'Online-Besichtigung möglich',
                                'Wohnberechtigungsschein erforderlich',
                                'Stufenloser Zugang',
                                'Online-Besichtigung',
                                'Einbauküche'
                                ]

    def get_listings(self, 
        shape_id = 'e3BsX0l1ZGBwQWpvQG9NZ0RrdUFoeUB8TH5Ab1tgbUBjdEBsTGVzQWFFY1B6TGdJbE1nUnxKYUNqSGJFckJsRGxNbk5wQ2NQekZfXGpMeVl7QnNHeUd5S2tSfVN9UW9rQGtGZXVAUHdAcFNteUB8Q3twQHBDb3BBeUppb0BnQGdfQHBRbUZwQXdNcEF9eEBoQmtwQGpNb1ViSHVQcFV1ZkB8U2NPaE99YkByQnNPcEF7SmhGYURwV3xFYkpjQXpoQGpaeFl7Un5OdVd2SnNXeEp9eEB9QnNHU3lZc1VzVndacUd7R2NBeUdmQ3NCfExtakBwYUFfVHhHZWpAZlB5SXFrQGdnQHZYZ1RiSGFHfUZ_T3NRa01xa0BfTm9Val5jfEByUWtfQWRFYVV5TmNjQHFOcWBAdV5oYUBxVHpLe1Z_VGNJYEB1TWNIb1N0R2tBeUNhTGZKZ1RySG9VcGtAX2JAamtAfVB7Y0B3SmNed0txXWVVZ1hjSX1Ua05nSX1RP29GYGRAcUJydEBHck13WGFDa2pBYkF9UnhKZUV2WHJAYnNAY0FadU5sW2tMck9xd0BsaEF9U2JoQXdDclFxTnx0QGhDaHBAWnJhQFV6YUByQXBsQGNBdFhpT3pJfkZ6TGxEcEdoQn5GdkJsTW1KcE5lQ2haZ0Z4WHlFektnQm5GZ0JoaEB9QG5rQHBBYlZqTXppQGpLcFVxYUBkckFSblZqXXxEYnRAdXVAelJpW3pKd0xwRm9NalliXmJLfExiZ0B2UXBRbltoR3JQX0R6bEBoQWRQelt8VUFSfUxge0F7SX5vQElod0B8QWRJblZuY0BwYkFlSX5dbkY.',
        rooms_min = 2,
        rooms_max = '',
        price_min = '',
        price_max = 1000,
        sqm_min = 50,
        sqm_max = '',
        ads_since = ''):
        if ads_since:
            try:
                ads_since = parse(ads_since).strftime("%Y-%m-%dT%H:%M:%S")
            except:
                print("Cannot parse time string. Setting to default value of 24 hours ago from now...")
                ads_since = ''

        if not ads_since:
            ads_since = (datetime.now() - timedelta(hours = 24)).strftime("%Y-%m-%dT%H:%M:%S")

        urlbase = 'https://www.immobilienscout24.de/Suche/shape/wohnung-mieten'

        params = [#'haspromotion=false',
        'numberofrooms=%s-%s'%(str(float(rooms_min)) if rooms_min else rooms_min, str(float(rooms_max)) if rooms_max else rooms_max),
        'price=%s-%s'%(str(float(price_min)) if price_min else price_min, str(float(price_max)) if price_max else price_max),
        'livingspace=%s-%s'%(str(float(sqm_min)) if sqm_min else sqm_min, str(float(sqm_max)) if sqm_max else sqm_max),
        'lastmodification=%s'%ads_since,
        'sorting=2',
        'enteredFrom=result_list#']

        print(params)

        main_url = "%s?shape=%s&%s"%(urlbase,shape_id,"&".join(params))

        self.driver.get(main_url)

        # time.sleep(5)
        # sys.exit()

        ads = self.driver.find_elements_by_class_name('result-list__listing')

        listings = []

        for ad in ads:
            try:
                listings.append(ad.find_element_by_tag_name('a').get_attribute('href'))
            except: continue

        print("%s listings found" % len(listings))

        return listings

    def contact_ad(self, link):

        contact_postfix = '#/basicContact/email'

        self.driver.get(link + contact_postfix)

        try:
            name = self.driver.find_element_by_xpath("//*[@data-qa='contactName']").get_attribute('innerHTML').strip()
        except:
            name = ''

        msg = """Hallo %s, 
        
Wir sind Anna und Aqeel, auf der Suche nach einem neuen Ort, den wir unser Zuhause in Berlin nennen können. 

Wir leben schon in Berlin. Anna arbeitet als Geschäftsplanungsanalystin bei Motorola Solutions. Ich arbeite hauptberuflich als Solutions Engineer bei einem Hi-Tech-Startup namens Mobius Labs in Mitte. 

Wir verdienen mehr als 8000 € Brutto Gehalt pro Monat. Alle Unterlagen können sie auf diesem Link finden:
https://drive.google.com/file/d/1pZ7WCJcT4ok8wIIKg1uPCzYJCDVfWvIi/view?usp=sharing  

Wir sind gute Mieter. Beide sind Nichtraucher und haben keine Haustiere. Unsere derzeitigen Vermieter beschreiben uns als zuverlässige, stille Mieter. Wir werden verantwortungsvoll mit der Wohnung umgehen. Gerne stellen wir für Empfehlungen den Kontakt zu unseren aktuellen Vermietern her. 

Da wir in Berlin wohnen und derzeit Home-Office betreiben, wäre eine Besichtigung an jedem Tag und zu jeder Zeit möglich. Wenn Sie weitere Fragen haben, stehen wir Ihnen gerne zur Verfügung. 

Wir werden diese Wohnung sehr gerne unser Zuhause nennen. 

Viele Grüße 
Anna & Aqeel
""" % name

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

        employment = {'id' : 'contactForm-employmentRelationship', 'val': 'WORKER'}
        income = {'id' : 'contactForm-income', 'val': 'OVER_2000_UPTO_3000'}
        documents = {'id' : 'contactForm-applicationPackageCompleted', 'val': 'true'}
        persons = {'id' : 'contactForm-numberOfPersons', 'val': 'TWO_PERSON'}


        submit_btn_css = '.contentContainer button.button-primary'

        fields = [msg_field, firstname, lastname, email, phone, street, house_no, plz, city]

        try:
            for field in fields:
                time.sleep(1)
                try:
                    self.driver.find_element_by_id(field['id']).clear()
                    self.driver.find_element_by_id(field['id']).send_keys(field['val'])
                except Exception as e:
                    print(field, e)
                    pass

            try:
                Select(self.driver.find_element_by_id(salutation['id'])).select_by_value(salutation['val'])
            except Exception as e:
                print("salutation", e)
                pass
            
            submit_text = self.driver.find_element_by_css_selector(submit_btn_css).find_element_by_tag_name('span').get_attribute('innerHTML').strip()            

            if submit_text == 'Weiter':

                el = self.driver.find_element_by_css_selector(submit_btn_css)#.find_element_by_xpath("..")
                ActionChains(self.driver).move_to_element(el).click().perform()

                e = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, submit_btn_css)))
                
                for field in [employment, income, documents, persons]:
                    try:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, field['id'])))
                        Select(self.driver.find_element_by_id(field['id'])).select_by_value(field['val'])
                    except Exception as e:
                        print(field)
                        print(e)
                        pass
                    #time.sleep(1)

                try:
                    if 'ng-empty' in self.driver.find_element_by_xpath("//*[@id='contactForm-hasPets.no']").get_attribute('class').split():
                        el = self.driver.find_element_by_xpath("//*[@for='contactForm-hasPets.no']")
                        ActionChains(self.driver).move_to_element(el).click().perform()
                except Exception as e:
                    print('pets: ', e)
                    pass

                try:
                    if 'ng-empty' in self.driver.find_element_by_xpath("//*[@id='moveInDateType.flex']").get_attribute('class').split():
                        el = self.driver.find_element_by_xpath("//*[@for='moveInDateType.flex']")
                        ActionChains(self.driver).move_to_element(el).click().perform()
                except Exception as e:
                    print('move_in: ', e)
                    pass
            
            try:
                if 'ng-empty' in self.driver.find_element_by_xpath("//*[@id='contactForm-privacyPolicyAccepted']").get_attribute('class').split():
                    el = self.driver.find_element_by_id('contactForm-privacyPolicyText')
                    ActionChains(self.driver).move_to_element(el).click().perform()
            except Exception as e:
                print('move_in: ', e)
                pass
            
            time.sleep(1)

            try:
                el = self.driver.find_element_by_css_selector(submit_btn_css)#.find_element_by_xpath("..")
                ActionChains(self.driver).move_to_element(el).click().perform()

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.status-confirm')))
            
            except Exception as e:
                print("couldn't submit")
                print(e)

            return datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), True

        except Exception as e:
            print("returning false")
            print(e)
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), False

    def get_ad_data(self, link):
        
        try:
            self.driver.get(link)

            vals = ast.literal_eval(self.driver.find_element_by_tag_name('s24-ad-targeting').get_attribute('innerHTML').strip())

            row = pd.Series(vals)
            row.index = [stringcase.titlecase(id[4:]) for id in row.index]

            row['Link'] = link

            try:
                _str = self.driver.find_element_by_xpath('//*[@id="is24-expose-premium-stats-widget"]/../script').get_attribute('innerHTML').strip()
                online_since = ast.literal_eval(re.findall(r'"\S*"', re.findall(r'exposeOnlineSince: "\S*"', _str)[0])[0])
                row['Online Since'] = online_since
            except:
                pass

            try:
                tag_elements = self.driver.find_element_by_class_name('boolean-listing').find_elements_by_tag_name('span')
                tags = []
                for e in tag_elements:
                    tags.append(e.get_attribute('innerHTML').strip())

                if "Balkon/ Terrasse" in tags:
                    row['Balcony'] = 'y'

                if "Personenaufzug" in tags:
                    row['Lift'] = 'y'

                if "Garten/ -mitbenutzung" in tags:
                    row['Garden'] = 'y'

                if "WG-geeignet" in tags:
                    row['WG Possible'] = 'y'

                if "Keller" in tags:
                    row['Cellar'] = 'y'

                if "Einbauküche" in tags:
                    row['Has Kitchen'] = 'y'
            except:
                pass

            try:
                title = self.driver.find_element_by_xpath('//*[@id="expose-title"]').get_attribute('innerHTML').strip()
                wbs1 = "mit wbs" in title.lower()
                wbs2 = "mit-wbs" in title.lower()
                wbs3 = "Wohnberechtigungsschein erforderlich" in tags
                wbs = wbs1 or wbs2 or wbs3
                row['WBS'] = 'y' if wbs else 'n'
            except:
                pass
                
            return row

        except:
            return False

    def close_crawler(self):
        self.driver.close()