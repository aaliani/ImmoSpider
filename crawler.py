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


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
CHROMEDRIVER_PATH = '/Applications/chromedriver'

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

# driver.close


        