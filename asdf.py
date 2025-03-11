import cloudscraper
import bs4
from cianparser.constants import STREET_TYPES, NOT_STREET_ADDRESS_ELEMENTS, FLOATS_NUMBERS_REG_EXPRESSION
from cianparser.helpers import define_price_data
from cianparser.helpers import define_location_data
from cianparser.helpers import define_rooms_count
from cianparser.helpers import define_author
from cianparser.helpers import define_specification_data
import pickle
from cianparser.helpers import union_dicts
from functools import partial
import time
import json
from datetime import datetime
import os
import sys
import cianparser
from cianparser.constants import CITIES
import re
import copy
import ai
from ai import data_ as dt
from ai import chain_prompt
from telegrambot import save_cache
import tracemalloc
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from telegrambot import save_cache_tg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fp = webdriver.FirefoxProfile(r'c:\Users\edwpo\AppData\Roaming\Mozilla\Firefox\Profiles\kdvnh6gc.default-release')
driver = webdriver.Firefox(fp)
driver.get("https://www.cian.ru")
import pdb; pdb.set_trace()
baba = driver.find_element(By.XPATH, "/html/body/header/div/div/div[1]/div/div[2]/div/a[2]").click() 

while True:
    try:
        driver.switch_to.window(driver.window_handles[1])
        break
    except:
        pass
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]")))

for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.TAG_NAME, "div"):
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.TAG_NAME, "div")[1].click() 
    print(i.text)
for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div[2]").find_elements(By.TAG_NAME, "div"):
    print(i.text)