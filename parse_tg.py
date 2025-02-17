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


#driver = webdriver.Firefox(executable_path=r"C:\Users\pcpcc\Documents\GitHub\sdafdsf\geckodriver.exe")

url_base = "https://t.me/s/"
channel_list = ['Flats_for_friend', 'arenda_moskva_mo']

JSON_FILE = "tg_posts.json"

def load_old(JSON_FILE=JSON_FILE):
    while True:
        try:

            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass

def parse_tg():
    while True:
       
        old_json = load_old()
        for channel in channel_list:
            post_list = []
            with webdriver.Firefox(executable_path=r"geckodriver.exe") as driver:
                
                try:
                    driver.get(url_base + channel)
                    baba = driver.find_element(By.XPATH, "/html/body/main")  
                    soup = BeautifulSoup(baba.get_attribute("innerHTML"), 'lxml') 
                    for i in soup.find_all("div", {"class":"tgme_widget_message text_not_supported_wrap js-widget_message"}):
                        post_dict = {}
                        post_dict['post_id'] = i['data-post']
                        post_dict['text'] = re.sub('\n+', '\n', i.text )
                        post_dict['link'] = "https://t.me/"+ i['data-post']+"?single"
                        post_list = post_list + [post_dict]         
                except:
                    import traceback
                    print(traceback.format_exc())
                
                    break
                break_flag = False
            
                if channel in old_json:
                    pass
                else:
                    old_json[channel] = []
               # import pdb; pdb.set_trace()
                if len(post_list) > 0:
                    if any(d['post_id'] == post_list[-1]['post_id'] for d in old_json[channel]):  
                        flag1 = False  
                        while True:
                            if(break_flag):
                                break
                            for j in range(-1, -len(post_list)-1, -1):
                                if(-len(post_list) == j):  
                                    break_flag = True
                                if any(d['post_id'] == post_list[j]['post_id'] for d in old_json[channel]):
                                        post_list.pop(j)
                                        break
                    for filtered_post in post_list:
                        global dt
                        addon, good_description = chain_prompt(data=dt, desc=post_dict["text"], type = 1,telegram=True)
                        filtered_post["addon"] = addon
                        filtered_post["good_description"] = good_description
                        dt = {
    'model': 'gpt-4o-mini', 
    'messages': [ {'role': 'user', 'content': r"{0} {1}"}
    ]}
                    old_json[channel] = old_json[channel] + post_list
                    save_cache_tg(post_list)
            while True:
                try:
                    print(3)
                    with open(JSON_FILE, "w", encoding='utf-8') as new_file:       
                        json.dump(old_json, new_file, ensure_ascii=False, indent = 6)
                    break
                except:
                    import traceback
                    print(traceback.format_exc())
        time.sleep(300)
parse_tg()