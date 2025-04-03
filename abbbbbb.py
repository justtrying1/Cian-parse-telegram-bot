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
class Sent(Exception): pass
skipped = 0
def offer_list_updated(offer_list ,disappeared, appeared):
   
    for d in disappeared:
        pass
    for i in range(len(disappeared)):
        for j in range(len(offer_list)):
            if offer_list[j]['url'] == disappeared[i]['url']:
                offer_list.pop(j)   
                break
   
   
    return offer_list + appeared


def get_image_data(block):
    img_list = {}
    d= 0
    for i in block.select_one("div[data-name=Gallery]").findAll("img"):
        img_list["image{}".format(d)] = i['src']
        d+=1
    if img_list == {}:
        return {"image0":"нет картинки"}
    return img_list



def city_dict():
    city_dict = dict()
    for i in CITIES:
        city_dict[i[0]] = i[1]
    
    return city_dict
city_dict = city_dict()



def return_non_repetitive_records(file1, file2): #old, new
    
    result = copy.deepcopy(file1) #old_json[i]
    result_ = copy.deepcopy(file2) #offer_list_global[i]
    d=0
    break_flag = False
    while True:
        if(break_flag):
            break
        flag = False  
        
        for i in range(len(result_)):
            if(len(result_)-1 == i):  
                break_flag = True
            for j in range(len(result)):        
                if result[j]['url'] == result_[i]['url'] :
                    
                    result.pop(j)
                    result_.pop(i)
                    flag = True     
                    break
            if(flag):
                break
    
    return result, result_ #disappeared, appeared

def filter_out(offer_list, old, i, break_flag):
    #break_flag = False
    print(datetime.now())
    if len(offer_list) > 0:
        if any(d['url'] == offer_list[-1]['url'] for d in old[str(i)]):  
            flag1 = False  
            while True:
                if(break_flag):
                    break
                #import pdb; pdb.set_trace()
                for j in range(-1, -len(offer_list)-1, -1):
                    if(-len(offer_list) == j):  
                        break_flag = True
                    if any(d['url'] == offer_list[j]['url'] for d in old[str(i)]):
                            offer_list.pop(j)
                            
                            break


OLD_JSON = r"&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
def load_old():
    while True:
        try:

            with open(OLD_JSON, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            print("old except")
def get_urls(i, min_price, max_price, city, deal_type,room2=0, room1=1, page=1, room3=0, no_room = False, preload = False):
    url_list=[]
    time.sleep(3.5)
    offer_list = []
    session = cloudscraper.create_scraper()
    if no_room:
        url_base = partial("https://www.cian.ru/cat.php?currency=2&p={page}&deal_type={deal_type}&engine_version=2&sort=creation_date_desc&maxprice={max_price}&minprice={min_price}&offer_type=flat&region={city_id}&room0={room0}&type=4".format, max_price=max_price, 
                       min_price=min_price, 
                       city_id=city_dict[city], 
                       deal_type=deal_type, 
                       room0=1)
    else:
        url_base = partial("https://www.cian.ru/cat.php?currency=2&p={page}&deal_type={deal_type}&engine_version=2&sort=creation_date_desc&maxprice={max_price}&minprice={min_price}&offer_type=flat&region={city_id}&room1={room1}&room2={room2}&room3={room3}&type=4".format, max_price=max_price, 
                        min_price=min_price, 
                        city_id=city_dict[city], 
                        deal_type=deal_type, 
                        room1=room1, 
                        room2=room2,
                        room3=room3)
    flag = False
    while True:
       # import pdb; pdb.set_trace()
        with cloudscraper.create_scraper() as session:

            try:
            
                res = session.get(url_base(page=page), headers={'Accept-Language': 'en'})
            except:
                continue
            list_soup = bs4.BeautifulSoup(res.text, "html.parser")
            offers = list_soup.select("article[data-name='CardComponent']")
            if (res.url.find("p=1&") != -1) & (page != 1):
            
                flag = True
            
                page = page - 1
                res = session.get(url_base(page=page))     
        list_soup = bs4.BeautifulSoup(res.text, "html.parser")
        offers = list_soup.select("article[data-name='CardComponent']")
        if(offers == []):
            time.sleep(3)
            print("0")
            get_urls(i, min_price=i*5000, room1=room1, room2=room2, max_price=((i+1)*5000)-1, city=city, room3=room3, deal_type="rent",no_room=no_room, preload=preload)
            
            return
        for offer in offers:
                common_data = dict()
                if deal_type == "sale":
                    pricing_type = "price"
                else:
                    pricing_type = "price_per_month"
                try:
                    price = define_price_data(offer)
                except:
                    price = {pricing_type : (min_price//2 + max_price//2)}
               
                price_compare = price[pricing_type]
                
                if(min_price <= price_compare <= max_price):
                    
                    try:
                            #import pdb; pdb.set_trace()
                            if not preload:
                                common_data['preload'] = 0
                            else:
                                common_data['preload'] = 1

                            common_data['metro_dist'] = offer.find_all("div", {"class":"_93444fe79c--remoteness--q8IXp"})[0].text
                            
                    except IndexError:
                        if (offer.select('div[data-name="SpecialGeo"]') == []):
                             common_data['metro_dist'] = '6666'
                        #import pdb; pdb.set_trace()
                    common_data['title'] = offer.select('div[data-name="GeneralInfoSectionRowComponent"]')[0].select("span")[1].text
                    common_data['description'] = offer.select('div[data-name="Description"]')[0].select("p")[0].text
                    common_data['url'] = offer.select("div[data-name='LinkArea']")[0].select("a")[0].get('href')
                    common_data['time'] = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
                    try:
                        common_data['geolabel'] = offer.select("a[data-name=GeoLabel]")[1].text
                    except:
                        common_data['geolabel'] = ".*"
        
                    location_data = define_location_data(offer, False)
                    price_data = price
                    author_data = define_author(offer)
                    
                    specification_data = define_specification_data(offer)
                   
                    try:
                        image_data = get_image_data(offer)
                    except:
                        image_data = {'image0':" "}

                    offer_list = offer_list + [union_dicts(author_data, specification_data, price_data, location_data, common_data, image_data, addon=[])]
                    url_list.append((offer.select("div[data-name='LinkArea']")[0].select("a")[0].get('href')))
        old = load_old()
        if str(i) in old:
            pass
        else:
            old[str(i)] = []

        break_flag = False
        if not preload:
       
            if len(offer_list) > 0:
                if any(d['url'] == offer_list[-1]['url'] for d in old[str(i)]):  
                    flag1 = False  
                    while True:
                        if(break_flag):
                            break
                        #import pdb; pdb.set_trace()
                        for j in range(-1, -len(offer_list)-1, -1):
                            if(-len(offer_list) == j):  
                                break_flag = True
                            if any(d['url'] == offer_list[j]['url'] for d in old[str(i)]):
                                    offer_list.pop(j)
                                    break
        print(datetime.now())
        page += 1
        url_list = list(dict.fromkeys(url_list))
        if(flag or (page == 4) or break_flag): 
            if preload:
                if len(offer_list) > 0:
                    if any(d['url'] == offer_list[-1]['url'] for d in old[str(i)]):  
                        flag1 = False  
                        while True:
                            if(break_flag):
                                break
                            #import pdb; pdb.set_trace()
                            for j in range(-1, -len(offer_list)-1, -1):
                                if(-len(offer_list) == j):  
                                    break_flag = True
                                if any(d['url'] == offer_list[j]['url'] for d in old[str(i)]):
                                        offer_list.pop(j)
                                        
                                        break
            if no_room and not preload:               
                if len(offer_list) > 100:
                    global skipped
                    skipped  = skipped + len(offer_list)
                if len(offer_list) <= 100:        
                    for filtered_offer in offer_list:
                        #import pdb; pdb.set_trace()

                        global dt
                        addon, good_description = chain_prompt(data=dt, desc=filtered_offer["description"], type = 1)
                        filtered_offer["addon"] = addon
                        filtered_offer["good_description"] = good_description
                        dt = {
    'model': 'gpt-4o-mini', 
    'messages': [ {'role': 'user', 'content': r"{0} {1}"}
    ]
}
            
            
            offer_list = list({v['url']:v for v in offer_list}.values())

            global offer_list_global
            offer_list_global[str(i)] = offer_list
            break


def parse( i_min, i_max, preload=False, room1=1, room2=0, room3=0, no_room=False):

    first_time = True
                        
    global offer_list_global
    offer_list_global = {}
    #offer_list = []        
    #import pdb; pdb.set_trace()
    for i in range(i_min, i_max):
        get_urls(i, min_price=i*5000, max_price=((i+1)*5000)-1, city="Москва", deal_type="rent",room2=room2,room1=room1,no_room=no_room,room3=room3, preload=preload)
    
        location_ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname("goo.py")))
        try:
            for root, dirs, files in os.walk(location_):
                for file in files:
                    if re.match(r'&.*\.json$', file):
                        #os.rename(file, str(file)[1:])
                        filename = file
                        with open(str(file), "r", encoding='utf-8') as old:
                            old_json = json.load(old)
                            if str(i) in old_json:
                                pass
                                #disappeared, appeared  = return_non_repetitive_records(old_json[str(i)], offer_list_global[i])
                            else:
                                old_json[str(i)] = []
                                disappeared = []
                                appeared = []
                            disappeared = []
                            #import pdb; pdb.set_trace() 
                            flagger = False  
                            old_json[str(i)] = offer_list_updated(offer_list=old_json[str(i)], disappeared=disappeared, appeared=offer_list_global[str(i)]) 
                            
                            
                            if(not flagger and len(offer_list_global[str(i)]) > 0 and not preload):       
                                print(2)
                                #import pdb; pdb.set_trace()
                               # pass
                                save_cache(offer_list_global[str(i)][:-len(offer_list_global[str(i)])+50])
                            
                            while True:
                                try:
                                    print(3)
                                    with open(filename, "w", encoding='utf-8') as new_file:       
                                        json.dump(old_json, new_file, ensure_ascii=False, indent = 6)
                                    break
                                except:
                                    import traceback
                                    print(traceback.format_exc())
                                    pass
                            
                            
                            
                            raise Sent
        except Sent:
            pass
import traceback
import gc
#parse(2,25,room1=1,room2=1, no_room=True, preload=True) # NO ROOOOOOOOM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#parse(2,30,room1=1,room2=1, room3=1, no_room=False, preload=True)   # YES ROOOOOOM!!!!!!!!!!!!!!!!!!!!!
tracemalloc.start()
while True:
    then = datetime.now()
   # parse(2,10,room1=0,room2=0, no_room=True)    
   # parse(2,10,room1=1,room2=1, no_room=False)    
    parse(5,25,room1=1,room2=1, room3=1)
    print(datetime.now() - then )
    print("skipped " + str(skipped))
    skipped = 0
    time.sleep(15)
    print(tracemalloc.get_traced_memory())
    gc.collect()
   
    
   ## except:
   #     print("error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
