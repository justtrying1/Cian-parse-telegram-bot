import cloudscraper
import bs4
from cianparser.constants import STREET_TYPES, NOT_STREET_ADDRESS_ELEMENTS, FLOATS_NUMBERS_REG_EXPRESSION
from cianparser.helpers import define_price_data
from cianparser.helpers import define_location_data
from telebot import types
from cianparser.helpers import define_rooms_count
from cianparser.helpers import define_author
from cianparser.helpers import define_specification_data
import pickle
from cianparser.helpers import union_dicts
from functools import partial
import time
import json
from datetime import datetime
import telebot
SNIMATEL_API = "7848749485:AAGSP-D5jD0d0JflbZCTXhMe3mKt6DP8NC0"
snimatel_robot = telebot.TeleBot(SNIMATEL_API)
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
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from telegrambot import save_cache_tg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
OLD_JSON = r"&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
def load_old():
    while True:
        try:

            with open(OLD_JSON, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass


fp = webdriver.FirefoxProfile(r'kdvnh6gc.default-release')

def load_cookie(driver, chat_id):
    with open('{}.pkl'.format(chat_id), 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

def hello_rieltor(cian_link="", chat_id = 123):
    driver = webdriver.Firefox()
    driver.get("https://cian.ru")
    load_cookie(driver, chat_id)
    driver.get(cian_link)
    counter = 0

            #time.sleep(10)
    if counter  > 150:
            return
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[.='Написать']"))).click()   # кнопка "написать" на странице объявления
        counter = counter+1
    except:
        driver.close()
        return False
        

    break_flag = False
    while True:
            # Получить текущий фокусированный элемент
            ActionChains(driver).send_keys(Keys.TAB).perform()
            focused_element = driver.execute_script("return document.activeElement;")
            
            # Получить информацию о фокусированном элементе
            tag_name = focused_element.get_attribute('tagName')
            class_name = focused_element.get_attribute('className')
            element_id = focused_element.get_attribute('id')
            inner_text = focused_element.text
            
            # Очистить консоль (в терминале это просто не выводить предыдущие строки)
            print("033c", end="")  # ANSI escape code для очистки терминала
            
            if tag_name == "IFRAME":
                if not break_flag:
                    element = driver.find_element(By.CLASS_NAME, class_name)
                    
                    try:
                        element.find_elements(By.XPATH, '//span[@data-name="HintQuestion"]')[1].click()
                    except:
                            pass
                            #import pdb; pdb.set_trace()
                
                if break_flag:
                # import pdb; pdb.set_trace()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                    ActionChains(driver).send_keys(Keys.ENTER).perform()
                    driver.close()
                    return True
                    break
                break_flag = True
            # Вывести информацию о фокусированном элементе
            print("Элемент с фокусом:")
            print(f"Tag Name: {tag_name}")
            print(f"Class Name: {class_name}")
            print(f"ID: {element_id}")
            print(f"Inner Text: {inner_text}")
            driver.close()
           
def auau():
    chat_id = "cookies"
    driver = webdriver.Firefox()
    load_cookie(driver, chat_id)
    old = load_old()
    for i in old:
        if int(i) < 6:
             continue
        for ad in old[i][::-1]:
                time.sleep(10)
                if counter  > 150:
                     return
                driver.get(ad['url'])
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[.='Написать']"))).click()   # кнопка "написать" на странице объявления
                    counter = counter+1
                except:
                    continue

                break_flag = False
                while True:
                        # Получить текущий фокусированный элемент
                        ActionChains(driver).send_keys(Keys.TAB).perform()
                        focused_element = driver.execute_script("return document.activeElement;")
                        
                        # Получить информацию о фокусированном элементе
                        tag_name = focused_element.get_attribute('tagName')
                        class_name = focused_element.get_attribute('className')
                        element_id = focused_element.get_attribute('id')
                        inner_text = focused_element.text
                        
                        # Очистить консоль (в терминале это просто не выводить предыдущие строки)
                        print("033c", end="")  # ANSI escape code для очистки терминала
                        
                        if tag_name == "IFRAME":
                            if not break_flag:
                                element = driver.find_element(By.CLASS_NAME, class_name)
                                
                                try:
                                    element.find_elements(By.XPATH, '//span[@data-name="HintQuestion"]')[1].click()
                                except:
                                     pass
                                     #import pdb; pdb.set_trace()
                            
                            if break_flag:
                            # import pdb; pdb.set_trace()
                                ActionChains(driver).send_keys(Keys.TAB).perform()
                                ActionChains(driver).send_keys(Keys.ENTER).perform()
                                
                                break
                            break_flag = True
                        # Вывести информацию о фокусированном элементе
                        print("Элемент с фокусом:")
                        print(f"Tag Name: {tag_name}")
                        print(f"Class Name: {class_name}")
                        print(f"ID: {element_id}")
                        print(f"Inner Text: {inner_text}")

                        time.sleep(0)  # Проверка каждые 500 миллисекунд


#def get_chats_amount():
   


DIALOGUES_FILE = "dialogues.json"
def load_dialogues():
    if os.path.exists(DIALOGUES_FILE):
        with open(DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_dialogues(params):
    with open(DIALOGUES_FILE, 'w', encoding='utf-8') as file:
        json.dump(params, file, ensure_ascii=False)

from deepseek import data_, cian, dialogue
user_data = load_dialogues()
data_['messages'].append({"role": "assistant", "content":"{}".format("Здравствуйте. Уточните, пожалуйста, ещё сдаёте?")})
import traceback
# Получение информации о текущем элементе с фокусом
def answer_vstrecha(chat_id, flat_id, message):
    global user_data
    driver = webdriver.Firefox()
    load_cookie(driver, chat_id)
    driver.get("https://www.cian.ru")
    baba = driver.find_element(By.XPATH, "/html/body/header/div/div/div[1]/div/div[2]/div/a[2]").click() 

    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            break
        except:
            pass
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]")))
  #  import pdb; pdb.set_trace()
    time.sleep(3)
    print(len(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]')))

    while True:
       # import pdb; pdb.set_trace()
        flag = False
        for i in driver.find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
            if i.text.split('\n')[0] == "Циан":
                continue
            print(i.get_attribute('data-chatid'))
            try:
                if int(i.get_attribute('data-chatid').split("_")[-1]) == flat_id:
                    
                    i.click()
                    user_data[chat_id][flat_id] ['messages'].append({"role":"assistant", "content":"{}".format(message)})
                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys(message) 
                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click()
            except:
                pass

def chat_list_monitoring(chat_id):
    
    
    global user_data
    driver = webdriver.Firefox()
    driver.get("https://cian.ru")
    load_cookie(driver, chat_id)
    driver.get("https://www.cian.ru")
    baba = driver.find_element(By.XPATH, "/html/body/header/div/div/div[1]/div/div[2]/div/a[2]").click() 

    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            break
        except:
            pass
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]")))
  #  import pdb; pdb.set_trace()
    time.sleep(3)
    print(len(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]')))

    while True:
       # import pdb; pdb.set_trace()
        flag = False
        for i in driver.find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
            if i.text.split('\n')[0] == "Циан":
                continue
            print(i.get_attribute('data-chatid'))
            try:
                flat_id = int(i.get_attribute('data-chatid').split("_")[-1])
                
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                if flat_id not in user_data[chat_id]:
                    user_data[chat_id][flat_id] = data_
                elif user_data[chat_id][flat_id]['status'] == "negated":
                    continue
            except:
                pass
            try:
                number_of_messages = int(i.text.split("\n")[-1])
              
                message = ""
                i.click()
                while True:
                    try:
                        for msg in driver.find_elements(By.XPATH, '//div[@data-name="ChatMessageLayout"]')[-number_of_messages:]:
                            message =  "{0} \n".format(message).join(msg.text.split('\n')[:-1])
                        break
                    except:
                        print(traceback.format_exc())
                user_data[chat_id][flat_id] ['messages'].append({"role":"user", "content":"{}".format(message)})
                response = dialogue(user_data[chat_id][flat_id])
                if "vstrecha" in response:
                    button = types.InlineKeyboardButton('Ответить', callback_data="vstrecha {}".format(flat_id))
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(button)
                    snimatel_robot.send_message(chat_id, "Автор объявления {0} прислал следующее сообщение: {1} \n Когда бы вам было удобно назначить встречу?".format("https://www.cian.ru/rent/flat/{}/".format(flat_id), message), reply_markup=keyboard)
                    
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys(response) 
                
                time.sleep(2)
                user_data[chat_id][flat_id] ['messages'].append({"role":"assistant", "content":"{}".format(response)})
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click()
                time.sleep(2)
                flag = True

                break
            except:
                continue


        driver.refresh() 
        save_dialogues(user_data)
        if not flag:
            time.sleep(300)

# driver.find_element(By.XPATH, '//div[@data-name="ChatListItem"]').get_attribute('data-chatid') 
# driver.find_element(By.XPATH, '//div[@data-name="ChatListItem"]').text.split("\n")[-1] 

#driver.find_element(By.CLASS_NAME, "a10a3f92e9--iframe--wECQa").find_elements(By.XPATH, '//button')[1].click()     
# Получение информации о последнем элементе, на который вы кликнули

#import pdb; pdb.set_trace()


#WebDriverWait(driver, 20).until(EC.presence_of_element_located(By.XPATH, "//textarea[@placeholder='Написать сообщение']"))
#driver.find_elements(By.XPATH, '//span[@data-name="HintQuestion"]')[1].click() # еще сдаете? клик
    
#driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/span") # Chat header

#for i in driver.find_elements(By.XPATH, "/html/body/div/div/div[1]/div[2]/div"):
#    print(i.text)

#


#auau()

   
if __name__ == "__main__":
    chat_list_monitoring()

#data['amount_after'] = get_chats_amount()


#for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
    #print(i.text)

#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.TAG_NAME, "div")[1].click() 
#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div[2]")))
#for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]").find_elements(By.XPATH, '//div[@data-name="ChatPageLayout"]'):
   # print(i.text)
#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys("123123") 
#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click() 