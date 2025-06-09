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
from telegrambot import bot
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
from ai import data_, cian, dialogue

DIALOGUES_FILE = "dialogues.json"
_DIALOGUES_FILE = "_dialogues.json"

def load_dialogues():

    if os.path.exists(DIALOGUES_FILE):
        with open(DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringA = json.load(file)
        with open(_DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringB = json.load(file)
        jsonMerged = {**jsonStringA, **jsonStringB}
        return jsonMerged
    return {}

def save__dialogues(params):
    with open(_DIALOGUES_FILE, 'w', encoding='utf-8') as file:
        json.dump(params, file, ensure_ascii=False)
def save_dialogues(params):
    with open(DIALOGUES_FILE, 'w', encoding='utf-8') as file:
        json.dump(params, file, ensure_ascii=False)

user_data = load_dialogues()
#data_['messages'].append({"role": "assistant", "content":"{}".format("Здравствуйте. Уточните, пожалуйста, ещё сдаёте?")})

OLD_JSON = r"&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
def load_old():
    while True:
        try:

            with open(OLD_JSON, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass


#fp = webdriver.FirefoxProfile(r'kdvnh6gc.default-release')

def load_cookie(driver, chat_id):
    with open('{}.pkl'.format(chat_id), 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
two_males_message = "Не пугайтесь, что вы так быстро видите это сообщение, это не спам, просто я айтишник и отправляю его всем подходящим по цене и метро квартирам как только они появятся =). Меня зовут Илья заинтересовала ваша квартира Снимать планируем вдвоем, я и мой друг. Мне 25 лет, другу 27, гражданство РФ, занятость в IT, доход стабильный, чистоту квартиры гарантируем, можно ли посмотреть квартиру в ближайшее время?"
animals_message = "Здравствуйте, понравилась ваше объявление. Обо мне: зовут Ольга, 27 лет, родом из Санкт-Петербурга, работаю в консалтинговой фирме с оплатой проблем не будет, люблю когда в квартире чисто, регулярно убираюсь. Есть кот: кастрированный и очень умный сибирской породы, приучен к котгеточке - мебель не дерёт, могу прислать фотку. В общем, надеюсь на ваше понимание."

def hello_rieltor(cian_link="", chat_id = 123, delay = 0):
    time.sleep(delay)
    #import pdb; pdb.set_trace()
    
    global user_data
    chat_id = str(chat_id)
    flat_id = cian_link.split("/")[-2]
 
    from autosms import register_cian
    import os.path
    if not os.path.isfile("{}.pkl".format(chat_id)):
        register_cian(chat_id=chat_id)
    
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.get("https://cian.ru")
    load_cookie(driver, chat_id)
    driver.get(cian_link)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[.='Написать']"))).click()   # кнопка "написать" на странице объявления
        
    except:
        print(traceback.format_exc())
        #bot.send_message(int(chat_id), "Не удалось написать автору объявления.. Либо объявления не существует, либо автор принимает только звонки")
        driver.quit()
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
                        print(traceback.format_exc())
                            #import pdb; pdb.set_trace()
                
                if break_flag:
                    #import pdb; pdb.set_trace()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                    time.sleep(3)
                    ActionChains(driver).send_keys(Keys.ENTER).perform()
                    time.sleep(3)
                   # user_data[chat_id][flat_id] = data_.copy()
                   # save_dialogues(user_data)
                    driver.get("https://www.cian.ru/dialogs")
    
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]")))
                    time.sleep(3)
                    print(len(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]')))
                    import pdb; pdb.set_trace()
                    while True:
                        flag = False
                        for i in driver.find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
                            if i.text.split('\n')[0] == "Циан":
                                continue
                            print(i.get_attribute('data-chatid'))
                            try:
                                flat__id = i.get_attribute('data-chatid').split("_")[-1]
                                if flat_id == flat__id:
                                    if chat_id not in user_data:
                                        user_data[chat_id] = {}
                                    if flat_id not in user_data[chat_id]:
                                        user_data[chat_id][flat_id] = data_.copy()
                                    elif user_data[chat_id][flat_id]['status'] == "negated":
                                        continue
                                    if chat_id == "two males":
                                        response = two_males_message
                                    if chat_id == "animals":
                                        response = animals_message
                                   # response = dialogue(user_data[chat_id][flat_id], desc=params[chat_id]['general description'])
                                    i.click()
                                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys(response) 
                                    
                                    time.sleep(2)
                                    if user_data[chat_id][flat_id] ['messages'][-1]['role'] == "user":
                                        user_data[chat_id][flat_id] ['messages'] = user_data[chat_id][flat_id] ['messages'] + [({"role":"assistant", "content":"{}".format(response)})]
                                    save_dialogues(user_data)
                                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click()
                                    time.sleep(2)
                                    flag = True
                                    break
                            except:
                                print(traceback.format_exc())
                        driver.quit()
                        
                        return True
                        break
                break_flag = True
            # Вывести информацию о фокусированном элементе
            print("Элемент с фокусом:")
            print(f"Tag Name: {tag_name}")
            print(f"Class Name: {class_name}")
            print(f"ID: {element_id}")
            print(f"Inner Text: {inner_text}")                 
def auau():
    chat_id = "cookies"
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
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
   




import traceback
# Получение информации о текущем элементе с фокусом
def answer_vstrecha(chat_id: int, flat_id: int, message):
    
    chat_id = str(chat_id)
    flat_id = str(flat_id)
    global user_data
    user_data[chat_id][flat_id]['vstrecha'] = "Клиент пишет: \n{message}"

    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.get("https://www.cian.ru")
    load_cookie(driver, chat_id)
    driver.get("https://www.cian.ru")
    baba = driver.find_element(By.XPATH, "/html/body/header/div/div/div[1]/div/div[2]/div/a[2]").click() 
    #import pdb; pdb.set_trace()
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
        flag = False
        for i in driver.find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
            if i.text.split('\n')[0] == "Циан":
                continue
            print(i.get_attribute('data-chatid'))
            try:
                if i.get_attribute('data-chatid').split("_")[-1] == flat_id:
                    
                    i.click()
                    user_data[chat_id][flat_id] ['messages'] = user_data[chat_id][flat_id] ['messages'] + [({"role":"assistant", "content":"{}".format(message)})]
                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys(message) 
                    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click()
                    break
            except:
                print(traceback.format_exc())
from telegrambot import load_parameters
params = load_parameters()
from telegrambot import load_edit, save_edit
def chat_list_monitoring(chat_id):
    chat_id = str(chat_id)
    global user_data
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.get("https://cian.ru")
    load_cookie(driver, chat_id)
    driver.get("https://www.cian.ru/dialogs")
   
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]")))
    time.sleep(3)
    print(len(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]')))
    #import pdb; pdb.set_trace()
    while True:
        flag = False
        for i in driver.find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
            if i.text.split('\n')[0] == "Циан":
                continue
            print(i.get_attribute('data-chatid'))
            try:
                flat_id = i.get_attribute('data-chatid').split("_")[-1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                if flat_id not in user_data[chat_id]:
                    user_data[chat_id][flat_id] = data_.copy()
                elif user_data[chat_id][flat_id]['status'] == "negated":
                    continue
            except:
                print(traceback.format_exc())
            try:
                number_of_messages = int(i.text.split("\n")[-1])
                #import pdb; pdb.set_trace()
                message = ""
                i.click()
                while True:
                    try:
                        for msg in driver.find_elements(By.XPATH, '//div[@data-name="ChatMessageLayout"]')[-number_of_messages:]:
                            message = message + "\n".join(msg.text.split('\n')[:-1]) + "\n"
                        break
                    except:
                        print(traceback.format_exc())
                if user_data[chat_id][flat_id] ['messages'][-1]['role'] == "assistant":
                    user_data[chat_id][flat_id] ['messages'] = user_data[chat_id][flat_id] ['messages'] + [({"role":"user", "content":"{}".format(message)})]
                import pdb; pdb.set_trace()
                response = dialogue(user_data[chat_id][flat_id], cian=True)
                
                edit = load_edit()
                url = "https://www.cian.ru/rent/flat/{}/".format(user_data[chat_id][flat_id])
                
                if "two males yes" in response:
                    for id in edit[url]['messages']:
                        bot.edit_message_text(id, edit[url]['messages'][id], edit[url]['text'].replace("Можно ли двум мужчинам: ждем ответа", "Можно ли двум мужчинам: да"))
                if "two males no" in response:
                    for id in edit[url]['messages']:
                        bot.edit_message_text(id, edit[url]['messages'][id], edit[url]['text'].replace("Можно ли двум мужчинам: ждем ответа", "Можно ли двум мужчинам: нет"))
                if "animals yes" in response:
                    for id in edit[url]['messages']:
                        bot.edit_message_text(id, edit[url]['messages'][id], edit[url]['text'].replace("Можно ли с животными: ждем ответа", "Можно ли с животными: да"))
                if "animals no" in response:
                    for id in edit[url]['messages']:
                        bot.edit_message_text(id, edit[url]['messages'][id], edit[url]['text'].replace("Можно ли с животными: ждем ответа", "Можно ли с животными: нет"))   
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys(response) 
                
                time.sleep(2)
                if user_data[chat_id][flat_id] ['messages'][-1]['role'] == "user":
                    user_data[chat_id][flat_id] ['messages'] = user_data[chat_id][flat_id] ['messages'] + [({"role":"assistant", "content":"{}".format(response)})]

                driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click()
                time.sleep(2)
                flag = True
                break
            except:
                print(traceback.format_exc())
                continue
        driver.refresh() 
        time.sleep(2)
        save_dialogues(user_data)
        if not flag:
            time.sleep(120)

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
    #import pdb; pdb.set_trace()
    import threading
    dialogues = load_dialogues()
    dialogues_keys = set(dialogues.keys())
    while True:
        for key in dialogues_keys:
            if (key == '7494874190'):
                threading.Thread(target=chat_list_monitoring, args=(int(key),)).start()
        dialogues = load_dialogues()
        dialogues_keys = set(dialogues.keys()) - dialogues_keys
        time.sleep(100)

#data['amount_after'] = get_chats_amount()


#for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.XPATH, '//div[@data-name="ChatListItem"]'):
    #print(i.text)

#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]").find_elements(By.TAG_NAME, "div")[1].click() 
#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div[2]")))
#for i in driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]").find_elements(By.XPATH, '//div[@data-name="ChatPageLayout"]'):
   # print(i.text)
#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/textarea[1]").send_keys("123123") 
#driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/button[2]").click() 