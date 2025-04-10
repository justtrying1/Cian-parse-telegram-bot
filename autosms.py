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
from telegrambot import bot
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from telegrambot import save_cache_tg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
import random, psutil, shutil, os, time
from selenium import webdriver
import pickle

# Запуск Firefox
driver = webdriver.Firefox()
api_key = "fA56fd8e5df62e31c3fde1cd2ddb9828"
service = "adv"
activationType = "0"
language = "ru-RU"
ref = "694306"
country = "0"
action = "getNumber"
url = r"https://api.sms-activate.ae/stubs/handler_api.php"

#https://api.sms-activate.ae/stubs/handler_api.php?api_key=$api_key&action=getStatus&id=$id get activation status
# 
# Переход на сайт
import requests
API_KEY = api_key  # Замените на ваш API-ключ
service = 'adv'   # Укажите сервис (например, "vk", "whatsapp" и т.д.)
import traceback

#import pdb; pdb.set_trace()

def register_cian(chat_id=123):
    bot.send_message(int(chat_id), "Регистрируем новый Циан аккаунт...")
    try:
        driver.get("http://www.cian.ru")
        time.sleep(3)
        try:
            driver.find_element(By.XPATH, "//button[@title='Закрыть']").click() 
        except:
            print(traceback.format_exc())
        
        driver.find_element(By.XPATH, "/html/body/header/div/div[2]/div[1]/div/a/span").click()
        
        response = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={API_KEY}&action=getNumber&service={service}')
        if response.status_code == 200:
            data = response.text.split(':')
            if data[0] == 'ACCESS_NUMBER':
                number = data[2]
                activation_id = data[1]
                print(f"Получен номер: {number}, ID активации: {activation_id}")
            else:
                print("Ошибка получения номера:", data)
        else:
            print("Ошибка запроса:", response.status_code)
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@name='tel']").send_keys(number)
        time.sleep(2)
        driver.find_elements(By.XPATH, '//span[@class="_25d45facb5--box--TSmoe _25d45facb5--box--aD_nX"]')[0].click()
        driver.find_elements(By.XPATH, '//span[@class="_25d45facb5--box--TSmoe _25d45facb5--box--aD_nX"]')[1].click()  
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//span[contains(text(), "Продолжить")]').click()
        except:
            driver.find_element(By.XPATH, '//span[contains(text(), "Создать аккаунт")]').click()
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Создать аккаунт")]').click() ))
        counter = 0
        while True:
            response = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={API_KEY}&action=getStatus&id={activation_id}')
            if response.status_code == 200:
                data = response.text.split(':')
                if data[0] == 'STATUS_OK':
                    code = data[1]
                    print(f"Код подтверждения: {code}")
                    break
                else:
                    print("Ошибка получения статуса:", data)
                    time.sleep(15)
                    counter = counter + 1
                    if counter > 10:
                        register_cian(chat_id=chat_id)
                        return
            else:
                print("Ошибка запроса:", response.status_code)
                time.sleep(10)
        
        driver.find_element(By.XPATH, "//input[@name='code']").send_keys(code)
        try:
            driver.find_element(By.XPATH, '//span[contains(text(), "Войти")]').click() 
        except:
            pass
        response = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={API_KEY}&action=setStatus&id={activation_id}&status=2')
        time.sleep(5)
        cookies = driver.get_cookies()
        with open('{}.pkl'.format(chat_id), 'wb') as file:
            pickle.dump(cookies, file)
        if response.status_code == 200:
            print("Номер успешно освобожден.")
        else:
            print("Ошибка освобождения номера:", response.status_code)
    except:
        print(traceback.format_exc())
       # import pdb; pdb.set_trace()



#register_cian()

# Загрузка куки из файла
def load_cookie():
    with open('7494874190.pkl', 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
#import pdb; pdb.set_trace()

# Обновление страницы для применения куки

# Теперь вы можете продолжать работу с сайтом