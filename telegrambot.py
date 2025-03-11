
#API_TOKEN = '7006315291:AAE_Nb6L-pNyVi5tFylMycjZnkAYrkkzyYs'  # Замените на ваш токен
API_TOKEN = '7535762439:AAFtiztp9pG3JsPnX7T7IRjuB6cQtqe5sno'
JSON_FILE_PATH = r'&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json'
import telebot
import json
import time
import os
import re
import datetime
from datetime import timedelta
from datetime import datetime
from copy import deepcopy
from telebot import types
import traceback

#API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

TINY_DB = {}
# Путь к локальному JSON-файлу
#JSON_FILE_PATH = 'ads.json'  # Укажите путь к вашему локальному JSON-файлу
#  # Используем множество для хранения уникальных URL объявлений
PARAMS_FILE = "params.json"
CACHE_FILE = "cache.json"
ACTION_FILE = "actions"
ACTION_FILE = "{ACTION_FILE}.json".format(ACTION_FILE=ACTION_FILE)
def load_action():
    try:
        if os.path.exists(ACTION_FILE):
            with open(ACTION_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}
    except:
        return {}
    

@bot.message_handler(commands=['buy'])
def buy(message):
    if message.from_user.id == 7494874190:
        activate_subscription(message)

    # Пример товара
    title = "Подписка на сервис"
    description = """Подходящие под Вас объявления с Циана✅ В течение 3-х минут после появления✅ Экономьте время и будьте первыми"""
    payload = "CUSTOM_PAYLOAD"  # Содержимое, которое будет отправлено обратно
    currency = "XTR"  # Валюта
    prices = [telebot.types.LabeledPrice("Двухнедельная подписка", 100)] 

    # Отправка запроса на оплату
    bot.send_invoice(
        chat_id=message.chat.id,
        title=title,
        description=description,
        currency=currency,
        invoice_payload=payload,
        provider_token=None,
        photo_url=None,
        photo_size=None,
        photo_width=None,
        photo_height=None,
        is_flexible=False,
        prices = prices
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Произошла ошибка")

@bot.message_handler(commands=['subscription'])
def check_subscription(message):
    state, msg = get_subscription_state(message.chat.id)
    bot.send_message(message.chat.id, msg)
        
        
def get_subscription_state(chat_id):
    all_params = load_parameters()
    now = datetime.now()
    msg = ""
    if "subscription" in all_params[str(chat_id)]:
        
        sub = all_params[str(chat_id)]['subscription']
    else:
        sub = all_params[str(chat_id)]['test_subscription']
    
    if (datetime.strptime(sub, '%d-%m-%Y  %H:%M:%S') - now).total_seconds() > 0:
        
        msg = msg + "Подписка активна до {}".format(sub) + "\n"
        return True, msg
    else:
        msg = msg + "Подписка истекла {}".format(sub) + "\n"
        return False, msg
   

def activate_subscription(message):
    chat_id = str(message.chat.id)
    all_params = load_parameters()

    all_params[chat_id]['subscription'] = (datetime.now() + timedelta(days=14)).strftime('%d-%m-%Y  %H:%M:%S')
    
    save_parameters(all_params)

    bot.send_message(int(message.chat.id), "Ваша двухнедельная подписка активирована")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    print("someone bought something")
    bot.send_message(message.chat.id,
                     'Ваш заказ выполнен, теперь ваша подписка активна, срок окончания подписки можно узнать с помощью команды /subscription')
                     
@bot.message_handler(commands=['refund'])
def refund_asked(message):
    if message.from_user.id == 7494874190:
        bot.send_message(message.chat.id, "asdfasfd")
        bot.register_next_step_handler(message, lambda msg : a(msg))

@bot.message_handler(commands=['test_subscription'])
def activate_test_subscription(message):
    #import pdb; pdb.set_trace()
    print("test sub activated")
    chat_id = str(message.chat.id)
    all_params = load_parameters()
    if 'test_subscription' not in all_params[chat_id]:

        all_params[chat_id]['test_subscription'] = (datetime.now() + timedelta(days=360)).strftime('%d-%m-%Y  %H:%M:%S')
        
        save_parameters(all_params)

      #  bot.send_message(int(message.chat.id), "Ваша трёхдневная подписка активирована")
    else:
        pass
      #  bot.send_message(int(message.chat.id), "Вы уже использовали активацию тестовой подписки")

def a(message):
    user_id = int(message.text)
    bot.refund_star_payment(user_id, "refund")

@bot.message_handler(commands=['transactions'])
def get_stars(message):
    print(message.from_user.id)
    if message.from_user.id == 7494874190:
        for i in bot.get_star_transactions().transactions:
            print(i) 
        bot.send_message(message.chat.id, str(bot.get_star_transactions()))    

def save_action(chat_id, action_name):
    #import pdb; pdb.set_trace()
    action = load_cache()
    if str(chat_id) not in action.keys():
        action[str(chat_id)] = {}
    action[str(chat_id)] = action_name
    with open(CACHE_FILE, 'w', encoding='utf-8') as file:
        json.dump(action, file, ensure_ascii=False)
    
def load_cache():
    with open(CACHE_FILE, "r", encoding='utf-8') as file:
       a = json.load(file)
    return a

def save_cache_tg(appeared):
  
    all_params = load_parameters()
    sent_list = {}
   # cache = load_cache()
    for i in all_params.keys():
        try:
            all_params[i]['mates']
        except:
            print(traceback.format_exc())
            continue

        if all_params[i] == {}:
            try:
                continue
            except:
                print(traceback.format_exc())
                continue
        
        chat_id = all_params.get(i)['chat_id']
        
        sent_list[chat_id] = str(len(appeared))
       
       
        if(len(appeared)) > 0:
            try:
                parsed_count = 0
                for ad in appeared:
                       
                    msg = f"источник: {"https://flatoon.pythonanywhere.com/?url="+ad['link'].split("https://")[1]}\n"
                    if 'addon' in ad:
                        parsed_addon = parse_addon(ad['addon'], params=all_params.get(i), good_description=ad['good_description'], telegram=True)
                        msg = parsed_addon + msg   
                    else:
                        parsed_addon = " "  
                    sub_flag = False
                    
                    if parsed_addon != " ":
                        parsed_count = parsed_count + 1 
                        print("addon parsed!")
                       
                        if ("test_subscription" not in all_params[i]) & ("subscription" not in all_params[i]):
                            sub_flag = True
                        elif get_subscription_state(chat_id)[0]:
                            bot.send_message(chat_id, msg)   
                        else:
                            sub_flag = True
                    elif chat_id == 7494874190:
                        bot.send_message(chat_id, ad['good_description']+"\n" + msg + "\n" + "\ncheck")
            
                
                if parsed_count > 0: 
                    button_bar = types.InlineKeyboardButton('Да', callback_data="i am here")
                    button_bar2 = types.InlineKeyboardButton('Нет', callback_data="i am no")
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(button_bar)
                    keyboard.add(button_bar2)
                    
                    if sub_flag:
                        bot.send_message(chat_id, "Чтобы получать новые объявления активируйте тестовую подписку с помощью /test_subscription или приобретите двухнедельную подписку с помощью команды /buy")
                    else:
                        if "answered" not in all_params.get(i).keys():

                            bot.send_message(chat_id, text='Нравится ли вам сервис?', reply_markup=keyboard)
                        bot.send_message(chat_id, text='Появилось {} новых объявления по вашему запросу, чтобы поменять параметры воспользуйтесь командой /start\n'    
                                        "".format(str(parsed_count)))
                
            except:
              #  if chat_id == 7494874190:
                   # import pdb; pdb.set_trace()
                print(traceback.format_exc())
                
           # save_action("sent", sent_list)
        
def save_cache(appeared):
  
    all_params = load_parameters()
    sent_list = {}
   # cache = load_cache()

    for i in all_params.keys():
       # import pdb; pdb.set_trace()
        if all_params[i] == "konchita":
            try:
                #bot.send_message(int(i), "Уважаемый пользователь, ваши данные были утеряны всвязи с техничискими неполадками, чтобы и дальше получать новые объявления пожалуйста пройдите заново регистрацию с помощью команды /start")
                continue
            except:
                
                print(traceback.format_exc())
                continue
        try:
            chat_id = all_params.get(i)['chat_id']
        except:
            continue
        new_filtered_ads = filter_ads(appeared, all_params.get(i))
        sent_list[chat_id] = str(len(new_filtered_ads))
       
        
        if(len(new_filtered_ads)) > 0:
             
           # import pdb; pdb.set_trace()            
            
            try:
              #  import pdb; pdb.set_trace()
                parsed_count = 0
                for ad in new_filtered_ads:
                  
                    
                    time_ = datetime.strptime(ad['time'], '%Y-%m-%d %H-%M-%S')
                    button_bar = types.InlineKeyboardButton('Показать описание', callback_data='{}'.format(ad['url']))
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(button_bar)
                    msg = f"""\nАктуально на {time_}\n
{ad['title']}
🚇метро: {ad['underground']} {ad['metro_dist']}
🧍‍♂️автор: {ad['author_type']}
💸цена: {ad['price_per_month']}₽
🏘район: {ad['district']}
🔗источник: {"https://flatoon.pythonanywhere.com/?url="+ad['url'].split("https://")[1]}\n
"""
                    if 'addon' in ad:
                        parsed_addon = parse_addon(ad['addon'], params=all_params.get(i), good_description=ad['good_description'])
                        msg = parsed_addon + msg    
                  #  import pdb; pdb.set_trace()
                    else:
                        parsed_addon = " "
                    
                    sub_flag = False
                    if (parsed_addon != " ") or ad['rooms_count'] > 0:
                        parsed_count = parsed_count + 1 
                        print("addon parsed!")
                    
                        if ("test_subscription" not in all_params[i]) & ("subscription" not in all_params[i]):
                            sub_flag = True
                        elif get_subscription_state(chat_id)[0]:
                            bot.send_message(chat_id, msg, reply_markup=keyboard)   
                        else:
                            sub_flag = True
                
                       
                    
                    elif chat_id == 7494874190:
                        if 'good_description' not in ad:
                            ad['good_description'] = " "
                        bot.send_message(chat_id, ad['good_description']+"\n" + msg + "\n")
            
                
                if parsed_count > 0: 
                    button_bar = types.InlineKeyboardButton('Да', callback_data="i am here")
                    button_bar2 = types.InlineKeyboardButton('Нет', callback_data="i am no")
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(button_bar)
                    keyboard.add(button_bar2)
                    
                    if sub_flag:
                        bot.send_message(chat_id, "Чтобы получать новые объявления активируйте тестовую подписку с помощью /test_subscription или приобретите двухнедельную подписку с помощью команды /buy")
                    else:
                        if "answered" not in all_params.get(i).keys():

                            bot.send_message(chat_id, text='Нравится ли вам сервис?', reply_markup=keyboard)
                        bot.send_message(chat_id, text='Появилось {} новых объявления по вашему запросу, чтобы поменять параметры воспользуйтесь командой /start\n'    
                                        "".format(str(parsed_count)))      
            except:
                print(traceback.format_exc())
       
def load_parameters():
    if os.path.exists(PARAMS_FILE):
        with open(PARAMS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Функция для сохранения параметров в файл
def save_parameters(params):
    with open(PARAMS_FILE, 'w', encoding='utf-8') as file:
        json.dump(params, file, ensure_ascii=False)

def get_chat_parameters(chat_id):
    all_params = load_parameters()
    return all_params.get(str(chat_id), None)
# Функция для загрузки объявлений из локального JSON
def load_ads(JSON_FILE_PATH=JSON_FILE_PATH):
    while True:
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
            break
        except:
            print(traceback.format_exc())
            

def send_old_ads_tg(message, params,dont_flag = 0, flag = False):
    all_params = params
    params = params[str(message.chat.id)]
    
    ads_to_filter = {}
    ads = load_ads(JSON_FILE_PATH="tg_posts.json")
    do_flag = False
   
    for segment in ads:
            for ad in ads[segment][-100:]:  
                if 'addon' in ad:
                    if segment not in ads_to_filter:
                        ads_to_filter[segment] = []
                    ads_to_filter[segment] = ads_to_filter[segment] + [ad]
    #import pdb; pdb.set_trace()
    for ads_segment in ads_to_filter:
        count = 0
        for ad in ads_to_filter[ads_segment][-100:]:
            
            msg = f"источник: {ad['link']}\n"
            if 'addon' in ad:
                parsed_addon = parse_addon(ad['addon'], params=params, good_description=ad['good_description'], telegram=True)
                msg = msg + parsed_addon  
            else:
                parsed_addon = " "
            if parsed_addon != " ":
                bot.send_message(message.chat.id, msg)
                count = count + 1 
                do_flag = True
            if count > 3 : #or (datetime.strptime(ad['time'], '%Y-%m-%d  %H-%M-%S') - datetime.now()).days > 10
                break
    if do_flag:
        if flag:
            #bot.send_message(message.chat.id, "К сожалению по вашему запросу не нашлось недавних объявлений. Поиск был расширен")
            pass
        else:
            pass
            #bot.send_message(message.chat.id, "Вот некоторые недавние объявления, которые могут подойти под ваш запрос, также я буду уведомлять Вас о всех новых объявлениях, как только они появятся. \n t.me/FlatoonChat - все-все-все объявления")
        #bot.send_message(message.chat.id, "Чтобы получать новые объявления необходимо выполнить активацию тестовой подписки с помощью команды /test_subscription")
        all_params[str(message.chat.id)] = params
        save_parameters(all_params)
    else:
        dont_flag = dont_flag + 1
        if dont_flag > 0:   
            params['author_type'] = "Любой"
        if dont_flag > 1:
            params['rooms'][0]['max_price'] = params['rooms'][0]['max_price'] + 2500
        if dont_flag > 3:
            params['undergrounds'] = ".*"
        if dont_flag > 4:
            return
        all_params[str(message.chat.id)] = params
        send_old_ads_tg(message, all_params,dont_flag, flag=True)
    
def send_old_ads(message, params,dont_flag = 0, flag = False):
    all_params = params
    params = params[str(message.chat.id)]
    ads_to_filter = {}
    ads = load_ads()
    do_flag = False
    for segment in ads:
            for ad in ads[segment][-100:]:  
                if 'addon' in ad or (ad['rooms_count'] > 0):
                    if segment not in ads_to_filter:
                        ads_to_filter[segment] = []
                    ads_to_filter[segment] = ads_to_filter[segment] + [ad]
    filtered_ads = {}
    for ads_segment in ads_to_filter:
        filtered_ads[ads_segment] = filter_ads(ads_to_filter[ads_segment], params)
    for ads_segment in filtered_ads:
       # import pdb; pdb.set_trace()
        count = 0
        for ad in filtered_ads[ads_segment][-100:]:
            msg = f"""{ad['title']}
🚇метро: {ad['underground']} {ad['metro_dist']}
🧍‍♂️автор: {ad['author_type']}
количество комнат: {ad['rooms_count']}
💸цена: {ad['price_per_month']}₽
🏘район: {ad['district']}
🔗источник: {ad['url']}\n
    """
            if 'addon' in ad :
                parsed_addon = parse_addon(ad['addon'], params=params, good_description=ad['good_description'])
                msg = msg + parsed_addon  
                        #  import pdb; pdb.set_trace()
            else:
                parsed_addon = " "
            
            if parsed_addon != " " or (ad['rooms_count'] > 0):
                bot.send_message(message.chat.id, msg)
                count = count + 1 
                do_flag = True
            if count > 3 or (datetime.strptime(ad['time'], '%Y-%m-%d  %H-%M-%S') - datetime.now()).days > 10:
                break
    if do_flag:
       
        if flag:
            bot.send_message(message.chat.id, "К сожалению по вашему запросу не нашлось недавних объявлений. Поиск был расширен")
        else:
            bot.send_message(message.chat.id, "Вот некоторые недавние объявления, которые могут подойти под ваш запрос, также я буду уведомлять Вас о всех новых объявлениях, как только они появятся.")
       
        all_params[str(message.chat.id)] = params
        save_parameters(all_params)
    else:
        dont_flag = dont_flag + 1
        if dont_flag > 0:   
            params['author_type'] = "Любой"
        if dont_flag > 1:
            params['rooms'][0]['max_price'] = params['rooms'][0]['max_price'] + 2500
        if dont_flag > 3:
            params['undergrounds'] = ".*"
        if dont_flag > 4:
            return
        all_params[str(message.chat.id)] = params
        send_old_ads(message, all_params,dont_flag, flag=True)

# Функция для фильтрации объявлений по цене и количеству комнат
def filter_ads(ads, criteria):
    filtered = []
    for ad in ads:       
        for room_criteria in criteria['rooms']:
            if ad['district'] == "":
                ad['district'] = "не указано"
            else:
                ad['district'] = ad['district'].lower()
            if ad['underground'] == "":
                ad['underground'] = "не указано"
            else:
                ad['underground'] = ad['underground'].lower()
            if ("geolabel" not in ad) or (ad['geolabel'] == "") :
                ad['geolabel'] = "не указано"
            else:
                ad['geolabel'] = ad['geolabel'].lower()
            
            try:
                dodo = (criteria['metro_dist'])
            except KeyError:
                criteria['metro_dist'] = 1000
            try:
                dodo = (criteria['author_type'])
            except KeyError:
                criteria['author_type'] = "Любой"
            if criteria['metro_dist'] == None:
                criteria['metro_dist'] = 1000
            if room_criteria['min_price'] == None:
                room_criteria['min_price'] = 0
            if room_criteria['max_price'] == None:
                room_criteria['max_price'] = 1000000000
                
            metro_dist = int(ad['metro_dist'].split(" ")[0])
            try:
                if  ("Владелец" in criteria['author_type']) and ad['author_type'] == "Владелец":
                    try:
                        if (metro_dist <= criteria['metro_dist'] + 8 and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and (list(filter(re.compile ( criteria['undergrounds'] ).match, ad['underground'])) or list(filter(re.compile ( criteria['undergronuds'] ).match, ad['geolabel'])) or list(filter(re.compile ( criteria['undergronuds'] ).match, ad['district'])) )):
                            filtered.append(ad)
                    except:    
                        print(traceback.format_exc())
                        if (metro_dist <= criteria['metro_dist'] + 8 and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and
                            ((list(filter(re.compile(ad['underground'].lower()).match, list(map(lambda x: x.lower(),criteria['undergrounds']))) or list(filter(re.compile ( ad['geolabel'] ).match, list(map(lambda x: x.lower(),criteria['undergrounds']))) or list(filter(re.compile ( ad['district'] ).match, list(map(lambda x: x.lower(),criteria['undergrounds']))))))))):
                        
                                filtered.append(ad)
                elif   "Владелец" not in criteria['author_type']:
                    try:
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and (list(filter(re.compile ( criteria['undergrounds'] ).match, ad['underground'])) or (list(filter(re.compile ( criteria['undergrounds'] ).match, ad['geolabel']))) or (list(filter(re.compile ( criteria['undergronuds'] ).match, ad['district']))))):
                            filtered.append(ad)
                    except:    
                        print(traceback.format_exc())
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and
                            (list(filter(re.compile(ad['underground']).match, list(map(lambda x: x.lower(),criteria['undergrounds'])))))or (list(filter(re.compile ( ad['geolabel'] ).match, list(map(lambda x: x.lower(),criteria['undergrounds'])))) or (list(filter(re.compile ( ad['district'] ).match, list(map(lambda x: x.lower(),criteria['undergrounds']))))))):
                        
                                filtered.append(ad)
                elif criteria['author_type'] == "Владелец" and ad['author_type'] != "Владелец":
                    break
            except KeyError:
                pass   
                print(traceback.format_exc())     
    return filtered
def filter_ads_tg(ads, criteria):
    filtered = []
    
    for ad in ads:       
        addon = ad['addon'][0] #!!!
        for room_criteria in criteria['rooms']:
            try:
                if  room_criteria['min_price'] <= int(addon['стоимость месячной аренды']) <= room_criteria['max_price']:
                    filtered.append(ad)
            except:
                print(traceback.format_exc())
    return filtered

def parse_addon(addon, params, good_description, strict=False, telegram=False):
    addon = addon[0]
    if any("двое" in a for a in params['sex']) and ((not any("Муж" in a for a in params['sex'])) or (not any ("Жен" in a for a in params['sex']))):
        params['sex'] = params['sex'] + ["Мужчина", "Женщина"]
    if not any("Один" in a for a in params['mates']) and not any("одного" in a for a in params['mates']):
        params['mates'].append("одного")
    
    flag = True
    if "сколько людей живёт в настоящий момент в квартире" in addon:
        addon["сколько людей живет в настоящий момент в квартире?"] = addon["сколько людей живёт в настоящий момент в квартире"] 
    try:
        if telegram:
            #import pdb; pdb.set_trace()
            if "классификация объявления" not in addon:
                raise Exception
            #elif ("поиск" in addon['классификация объявления']) and (not "поиск соседа" in addon['классификация объявления']):
            #    raise Exception
            if "сдача комнаты" not in addon["классификация объявления"]:
                addon['кто живёт в настоящий момент'] = {
                                    "никто": []
                              }
                addon["сколько людей живет в настоящий момент в квартире"] = 0
                if addon["стоимость месячной аренды"] == "не указано":
                    addon["стоимость месячной аренды"] = 0
            exc_flag = False
            rooms_list = []
            try: 
                for rooms in params['rooms']:      
                        rooms_list.append(rooms['rooms'])
                        if (("сдача студ" in addon['классификация объявления']) or ('сдача однок' in addon['классификация объявления'])) and (((1 == rooms['rooms']) and ((rooms['min_price']) <= addon['стоимость месячной аренды'] <= rooms['max_price']))):
                            raise Exception
                        if (("сдача двухкомнатной квартиры" in addon['классификация объявления'])) and (((2 == rooms['rooms']) and ((rooms['min_price']) <= addon['стоимость месячной аренды'] <= rooms['max_price']))):
                            raise Exception
                        if (("сдача трехкомнатной квартиры" in addon['классификация объявления']) and (((3 == rooms['rooms'])) and ((rooms['min_price']) <= addon['стоимость месячной аренды'] <= rooms['max_price']))):
                            raise Exception
                        if ("сдача комнаты" in addon['классификация объявления']) and (((0 == rooms['rooms']) and (rooms['min_price'] <= addon['стоимость месячной аренды'] <= rooms['max_price']))):
                            raise Exception
                        
            except:
                exc_flag = True
            finally:
                if not exc_flag:
                    raise Exception
         
      ##  if "не указано" in addon['можно ли заселиться с животными'] and not any("про животных" in a for a in params['animal']) and params['animal'] != []:
        #s    raise Exception
        if  (any("одного" in a for a in params['mates'])) or (((len(list(addon['кто живёт в настоящий момент'].values()))) == 1) and any("Один" in a for a in params['mates'])):
            print(len(list(addon['кто живёт в настоящий момент'].values())))
            mates = addon['кто живёт в настоящий момент']
            for mate in mates:
                if not any('никто' in a for a in  mates) or len(mates) != 1:
                    if (any("женщина" in a for a in [mate]) or any("женщина" in str(a) for a in addon['кто живёт в настоящий момент'][mate])) and not any("Женщины" in a for a in params['mates']) and any("Мужчины" in a for a in params['mates']):
                        raise Exception
                    if (any("мужчина" in a for a in [mate]) or any("мужчина" in str(a) for a in  addon['кто живёт в настоящий момент'][mate])) and not any("Мужчины" in a for a in params['mates']) and any("Женщины" in a for a in params['mates']):
                        raise Exception 
                    
                else:
                    pass
        else:
            raise Exception
    
        a = 0
        try:
            a = int(addon['сколько комнат в квартире'])
        except:
            pass
        if a !=0:
            if any("Один" in a for a in params['mates']) and not any("одного" in a for a in params['mates']) and int(addon['сколько комнат в квартире']) > 2 and any("не указано" in a for a in addon['кто живёт в настоящий момент']):
                print(addon)
                print("komnat v kvartire" + str(addon['сколько комнат в квартире']))
                raise Exception
            elif addon['сколько комнат в квартире'] == 1:
                addon['сколько комнат в квартире'] = "не указано"
        

        #if (any("мужчина" in a for a in addon['тип разыскиваемого жильца']) and any("Мужчина" in a for a in params['sex'])) or (any("женщина" in a for a in addon['тип разыскиваемого жильца']) and any("Женщина" in a for a in params['sex'])) or (any("человек" in a for a in addon['тип разыскиваемого жильца'])):
        #    pass
       # else:
            #import pdb;pdb.set_trace()
        #    raise Exception 
        all_net_general = "нет" in addon['ищут ли одного человека'] and ("нет" in addon['ищут ли двух человек'])
        all_net = (("нет" in addon["ищут ли пару из мужчины и женщины"]) and ("нет" in addon["ищут ли пару женщин/девушек"]) and "нет" in addon["ищут ли пару мужчин/парней"]  and "нет" in addon['ищут ли одного мужчину/парня'] and "нет" in addon['ищут ли одну женщину/девушку'])
        user_man = any("Муж" in a for a in params['sex']) and not any("Жен" in a for a in params['sex']) and not any("двое" in a for a in params['sex'])
        user_woman = not any("Муж" in a for a in params['sex']) and  any("Жен" in a for a in params['sex']) and not any("двое" in a for a in params['sex'])
        
        user_pair = any("Муж" in a for a in params['sex']) and any("Жен" in a for a in params['sex']) and any("двое" in a for a in params['sex'])
        user_guys =  any("Муж" in a for a in params['sex']) and not any("Жен" in a for a in params['sex']) and any("двое" in a for a in params['sex'])
        user_girls = not any("Муж" in a for a in params['sex']) and  any("Жен" in a for a in params['sex']) and any("двое" in a for a in params['sex'])
        if strict:
            pass
        if (user_man or user_woman) and (not "да" in addon['ищут ли одного человека'] and (not "да" in addon['ищут ли одного мужчину/парня']) and not "да" in addon['ищут ли одну женщину/девушку']) and "да" in addon['ищут ли двух человек']:
            raise Exception
        if (user_pair or user_guys or user_girls) and (not "да" in addon['ищут ли двух человек'] and ("не" in addon["ищут ли пару из мужчины и женщины"]) and ("не" in addon["ищут ли пару женщин/девушек"]) and "не" in addon["ищут ли пару мужчин/парней"]) and "да" in addon['ищут ли одного человека']:
            raise Exception
        if user_pair and "нет" in addon["ищут ли пару из мужчины и женщины"] and not all_net:
                raise Exception
        if user_guys and "нет" in addon["ищут ли пару мужчин/парней" ] and not all_net:
            raise Exception
        if user_girls and "нет" in addon["ищут ли пару женщин/девушек"] and not all_net:
            raise Exception
        if user_girls and ("не указано" in addon["ищут ли пару женщин/девушек"]) and (("да" in addon["ищут ли пару мужчин/парней"]) or "да" in addon["ищут ли пару из мужчины и женщины"] or "да" in addon['ищут ли одного мужчину/парня'] or "да" in addon['ищут ли одну женщину/девушку']):
            raise Exception
        if user_guys and "не указано" in addon["ищут ли пару мужчин/парней"] and (("да" in addon["ищут ли пару женщин/девушек"]) or "да" in addon["ищут ли пару из мужчины и женщины"]  or "да" in addon['ищут ли одного мужчину/парня'] or "да" in addon['ищут ли одну женщину/девушку']):
            raise Exception
        if user_pair and "не указано" in addon["ищут ли пару из мужчины и женщины"] and (("да" in addon["ищут ли пару женщин/девушек"]) or "да" in addon["ищут ли пару мужчин/парней"]  or "да" in addon['ищут ли одного мужчину/парня'] or "да" in addon['ищут ли одну женщину/девушку']):
            raise Exception
        if "не указано" in addon['ищут ли двух человек'] and not any("Жен" in a for a in params['sex']) and not any("Муж" in a for a in params['sex']) and any("двое" in a for a in params['sex']) and ("да" in addon['ищут ли одного мужчину/парня'] or "да" in addon['ищут ли одну женщину/девушку']):
            raise Exception
        if not user_man and not user_woman and "да" in addon['ищут ли двух человек'] and any("двое" in a for a in params['sex']):
            
            pass   
        
        elif  not user_man and not user_woman and ("да" in addon['ищут ли одного человека']) and any("двое" in a for a in params['sex']):
            raise Exception
        
        
        #import pdb;pdb.set_trace()
        
        if user_man and "нет" in addon['ищут ли одного мужчину/парня']:
            raise Exception
        
        if  user_woman  and "нет" in addon['ищут ли одну женщину/девушку']: 
            raise Exception
        
        if user_woman and  (("не указано" in addon['ищут ли одну женщину/девушку']) and ("да" in addon['ищут ли одного мужчину/парня'] or ("да" in addon["ищут ли пару мужчин/парней"]) or "да" in addon["ищут ли пару из мужчины и женщины"]  or "да" in addon["ищут ли пару женщин/девушек"])):
            raise Exception
        
        if user_man and  (("не указано" in addon['ищут ли одного мужчину/парня']) and "да" in addon['ищут ли одну женщину/девушку']  or (("да" in addon["ищут ли пару мужчин/парней"]) or "да" in addon["ищут ли пару из мужчины и женщины"]  or "да" in addon["ищут ли пару женщин/девушек"])):    
            raise Exception
        
        if not user_man and not user_woman and "да" in addon['ищут ли одного человека'] and not any("двое" in a for a in params['sex']):
            pass  
        if not user_man and not user_woman and "да" in addon['ищут ли двух человек'] and not any("двое" in a for a in params['sex']):
            raise Exception
       # import pdb; pdb.set_trace()
        if (any("кошка" in a for a in addon['можно ли заселиться с животными']) and any("Кошка" in a for a in params['animal'])) or (("cоба"in addon['можно ли заселиться с животными']) and any("Собака" in a for a in params['animal'])) or ("да" in addon['можно ли заселиться с животными']) or "не " in addon['можно ли заселиться с животными']:
            pass
        elif params['animal'] != []:
            #import pdb;pdb.set_trace()
            raise Exception
    except Exception as e:
        print(traceback.format_exc())
        flag = False
    msg = ""
    if flag:
       
        try:   
            msg = msg + "\n" + good_description
            
        except Exception as e:
            print(traceback.format_exc())
        
        #print(addon['кто живёт в настоящий момент'])
        return msg
    else:
        return " " #POPRAVm     
    
        
def format_time_passed(item_time):
    now = datetime.now()
    time_diff = now - item_time

    if time_diff < timedelta(minutes=1):
        return "только что"
    elif time_diff < timedelta(hours=1):
        minutes = time_diff.seconds // 60
        return f"{minutes} мин. назад"
    elif time_diff < timedelta(days=1):
        hours = time_diff.seconds // 3600
        return f"{hours} ч. назад"
    else:
        days = time_diff.days
        return f"{days} д. назад"
# Команда /start
def test_message(txt):
    for chat_id in load_parameters().keys():
        try:
            bot.send_message(int(chat_id),txt)
        except:
            pass

def main():
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
      #  import pdb; pdb.set_trace()
        global TINY_DB
        if "sub" in call.data:
            all_params = load_parameters()
           # import pdb; pdb.set_trace()
            try:
                bot.get_chat_member(chat_id=-1002495178490, user_id=call.message.from_user.id)
                send_old_ads_tg(call.message, all_params)
                send_old_ads(call.message, all_params)
            except:
                print(traceback.format_exc())
                keyboard = types.InlineKeyboardMarkup()
                button_bar = types.InlineKeyboardButton('Я подписался', callback_data='sub check')
                keyboard.add(button_bar)
                bot.send_message(chat_id=call.message.chat.id, text="Чтобы получить результаты поиска подпишитесь на канал @FlatoonChat", reply_markup=keyboard)
            
        if "i am" in call.data:
            all_params = load_parameters()
            params = all_params[str(call.message.chat.id)]
            
            #params = get_chat_parameters(call.message.chat.id)
            if "no" in call.data:
                params['answered'] = 0
                bot.send_message(call.message.chat.id, "Спасибо за отзыв. Пожалуйста, напишите о проблемах в работе боат в личные сообщения @milkicow, это поможет боту дальше развиваться")
            else:
                params['answered'] = 1
                bot.send_message(call.message.chat.id, "Спасибо за отзыв. Я очень рад, что сервис вам нравится, о любых недочётах можете написать в личные сообщения @milkicow, тогда вы поможете боту развиваться и дальше.")
            
            all_params[str(call.message.chat.id)] = params
            save_parameters(params=all_params)
        
            print("here" + str(call.message.chat.id))
        if 'startstart' in call.data:
            start_start(call.message)
        if 'sex' in call.data:
            
            keyboard = types.InlineKeyboardMarkup()
           # list = [types.InlineKeyboardButton('Двухкомнатные квартиры', callback_data='start 2'), types.InlineKeyboardButton('Однокомнатные квартиры', callback_data='start 1'), types.InlineKeyboardButton('Комнаты', callback_data='start 0')]
            list = [types.InlineKeyboardButton('Нас двое', callback_data='sex 3'), types.InlineKeyboardButton('Я один', callback_data='sex 2'), types.InlineKeyboardButton('Мужчина🤵‍♂️', callback_data='sex 1'), types.InlineKeyboardButton('Женщина👩‍🦱', callback_data='sex 0')]
            
            if call.data.split()[1] == "continue":
                get_mates(call.message)
                l = []
                for i in TINY_DB[call.message.chat.id]['sex_input']:
                    if i:
                        l.append(list.pop().text)
                    else:
                        list.pop()
                TINY_DB[call.message.chat.id]['sex_input'] = l
            else:
                TINY_DB[call.message.chat.id]['sex_input'][int(call.data.split()[1])] = not TINY_DB[call.message.chat.id]['sex_input'][int(call.data.split()[1])]
                
                for i in TINY_DB[call.message.chat.id]['sex_input']:
                    if not i:
                        keyboard.add(list.pop())
                    if i:
                        a = list.pop()
                        a.text = a.text + " ✅"
                        keyboard.add(a)
                button_bar = types.InlineKeyboardButton('Продолжить', callback_data='sex continue')
                keyboard.add(button_bar)   
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard) 
        
        if 'mate' in call.data:
            #import pdb; pdb.set_trace()
            keyboard = types.InlineKeyboardMarkup()
            list = [types.InlineKeyboardButton('Больше одного соседа 👯‍♂️👯‍♀️', callback_data='mate 3'), types.InlineKeyboardButton('Один сосед 🤼‍♂️', callback_data='mate 2'), types.InlineKeyboardButton('Мужчины 👨‍🦰', callback_data='mate 1'), types.InlineKeyboardButton('Женщины 👩‍🦱', callback_data='mate 0')]
            if call.data.split()[1] == "continue":
                get_animal(call.message)
                l = []
                for i in TINY_DB[call.message.chat.id]['mates_input']:
                    if i:
                        l.append(list.pop().text)
                    else:
                        list.pop()
                TINY_DB[call.message.chat.id]['mates_input'] = l
            else:
                TINY_DB[call.message.chat.id]['mates_input'][int(call.data.split()[1])] = not TINY_DB[call.message.chat.id]['mates_input'][int(call.data.split()[1])]
                
                for i in TINY_DB[call.message.chat.id]['mates_input']:
                    if not i:
                        keyboard.add(list.pop())
                    if i:
                        a = list.pop()
                        a.text = a.text + " ✅"
                        keyboard.add(a)
                button_bar = types.InlineKeyboardButton('Продолжить', callback_data='mates continue')
                keyboard.add(button_bar)   
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard) 
        if 'check_under' in call.data:
            if 'yes' in call.data:
                
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                check_undergrounds(call.message)
            if 'retry' in call.data:
                bot.send_message(call.message.chat.id, "*Через запятую* укажите автономный округ или станцию метро или район, пример: (СЗАО, НАО, Маяковская, Алексеевская")
                bot.register_next_step_handler(call.message, lambda msg: get_undergrounds(msg))
                
        if 'period' in call.data:
            #import pdb; pdb.set_trace()
            keyboard = types.InlineKeyboardMarkup()
            list = [types.InlineKeyboardButton('Долгий' , callback_data='period 1'), types.InlineKeyboardButton('Короткий ', callback_data='period 0')]
            if call.data.split()[1] == "continue":
                get_animal(call.message)
                l = []
                for i in TINY_DB[call.message.chat.id]['period_input']:
                    if i:
                        l.append(list.pop().text)
                    else:
                        list.pop()
                TINY_DB[call.message.chat.id]['period_input'] = l
            else:
                TINY_DB[call.message.chat.id]['period_input'][int(call.data.split()[1])] = not TINY_DB[call.message.chat.id]['period_input'][int(call.data.split()[1])]
                for i in TINY_DB[call.message.chat.id]['period_input']:
                    if not i:
                        keyboard.add(list.pop())
                    if i:
                        a = list.pop()
                        a.text = a.text + " ✅"
                        keyboard.add(a)
                button_bar = types.InlineKeyboardButton('Продолжить', callback_data='period continue')
                keyboard.add(button_bar)   
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard) 
        print(call.data)
        if 'animal' in call.data:
        #import pdb; pdb.set_trace()
            keyboard = types.InlineKeyboardMarkup()
            list = [types.InlineKeyboardButton('Собака🦮' , callback_data='animal 1'), types.InlineKeyboardButton('Кошка 🐈‍⬛', callback_data='animal 0')]
            
            if call.data.split()[1] == "continue":
                old_start(call.message)
                l = []
                for i in TINY_DB[call.message.chat.id]['animal_input']:
                    if i:
                        l.append(list.pop().text)
                    else:
                        list.pop()
                TINY_DB[call.message.chat.id]['animal_input'] = l
            else:
                TINY_DB[call.message.chat.id]['animal_input'][int(call.data.split()[1])] = not TINY_DB[call.message.chat.id]['animal_input'][int(call.data.split()[1])]
                print(TINY_DB[call.message.chat.id]['animal_input'][int(call.data.split()[1])])
                print(int(call.data.split()[1]))
                for i in TINY_DB[call.message.chat.id]['animal_input']:
                    if not i:
                        keyboard.add(list.pop())
                    if i:
                        a = list.pop()
                        a.text = a.text + " ✅"
                        keyboard.add(a)
                button_bar = types.InlineKeyboardButton('Продолжить', callback_data='animal continue')
                keyboard.add(button_bar)   
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard) 

        if 'max' in call.data:
            if 'continue' in call.data:
                #import pdb;pdb.set_trace()
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                get_undergrounds(call.message.chat.id)
        
        if 'dist' in call.data:
            if 'continue' in call.data:
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                get_metro_dist(call.message, skip=True)
        
        if 'author' in call.data:
            if 'continue' in call.data:     
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                get_author_type(call.message, skip=True)
            if 'yes' in call.data:
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                get_author_type(call.message, skip=False, author=True)
        
        if 'undergrounds' in call.data:
            if 'continue' in call.data:
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                get_undergrounds(call.message, skip=True)
                
        if 'start' in call.data:
           # import pdb;pdb.set_trace
          
            keyboard = types.InlineKeyboardMarkup()
            list = [types.InlineKeyboardButton('Трехкомнатные квартиры', callback_data='start 3'), types.InlineKeyboardButton('Двухкомнатные квартиры', callback_data='start 2'), types.InlineKeyboardButton('Однокомнатные квартиры', callback_data='start 1'), types.InlineKeyboardButton('Комнаты', callback_data='start 0')]
            #list = [types.InlineKeyboardButton('Комнаты', callback_data='start 0')]
            if call.data.split()[1] == "continue":
                get_rooms(call.message)
                #bot.register_next_step_handler(call.message, lambda msg: get_rooms(msg, rooms=TINY_DB[call.data.message.chat.id]))
            else:
                TINY_DB[call.message.chat.id]['rooms_input'][int(call.data.split()[1])] = not TINY_DB[call.message.chat.id]['rooms_input'][int(call.data.split()[1])]
                for i in TINY_DB[call.message.chat.id]['rooms_input']:
                    if not i:
                        keyboard.add(list.pop())
                    if i:
                        a = list.pop()
                        a.text = a.text + " ✅"
                        keyboard.add(a)
                button_bar = types.InlineKeyboardButton('Продолжить', callback_data='start continue')
                keyboard.add(button_bar)   
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard) 

        if "cian.ru" in call.data:
            try:
               # save_action(call.message.chat.id, 'desc')
                print(call.message.chat.id)
                #import pdb; pdb.set_trace()
                a = load_cache()
                msg = bot.send_message(call.message.chat.id, f"📔📔 Описание\n\n {a[str(call.message.chat.id)]['last 20'][call.data]}", reply_to_message_id=call.message.id)
                bot.pin_chat_message(chat_id=msg.chat.id, message_id=msg.message_id)
            except:
                print(traceback.format_exc())
            
        # button_foo = types.InlineKeyboardButton('Показать новые', callback_data='new')
    
    user_data = {}
    from ai import dialogue, a 

    @bot.message_handler(commands=['start'])
    def start(message):
       # import pdb; pdb.set_trace()
        params = load_parameters()
        try:
            if params[str(message.chat.id)] == "konchita":
                return
            if message.chat.id == 781665670:
                raise Exception
        except:
                
            bot.send_message(message.chat.id, "Бот просыпается ...")
            user_id = message.from_user.id
            user_data[user_id] =  {
        'model': 'gpt-4o-2024-08-06', 
        'messages': [ {'role': 'user', 'content': "{}".format(a)}
        ]}
        # import pdb; pdb.set_trace()
            if len(user_data[user_id] ['messages'])>1:
                user_data[user_id] ['messages'].append({"role":"user", "content":"{}".format(message.text)})
            response = dialogue(user_data[user_id] )
            user_data[user_id] ['messages'].append({"role": "assistant", "content":"{}".format(response)})
            bot.send_message(message.chat.id, "{}".format(response))
            bot.register_next_step_handler(message, lambda msg: cont(msg, data_=user_data[user_id]))
    

    def cont(message, data_):
        user_id = message.from_user.id
       # import pdb; pdb.set_trace()
        bot.send_message(message.chat.id, "Бот печатает ...")
        save_action(chat_id=message.chat.id, action_name=user_data[user_id])
        if len(user_data[user_id] ['messages'])>1:
            user_data[user_id] ['messages'].append({"role":"user", "content":"{}".format(message.text)})
        response = dialogue(user_data[user_id])
        if "ento konchita" in response:
            all_params = load_parameters()
        
            # Сохранение параметров для текущего чата
            all_params[str(message.chat.id)] = "konchita"
            save_parameters(all_params)
            save_action(chat_id=message.chat.id, action_name=user_data[user_id])
        if "beseda finita" in response:
            save_action(chat_id=message.chat.id, action_name=user_data[user_id])
            response, user_data[str(user_id) + "resp"] = response.split("beseda finita")
            try:
                params = json.loads(user_data[str(user_id) + "resp"])
                all_params = load_parameters()
                all_params[str(message.chat.id)] = params
                params['username'] = message.from_user.username
                params['chat_id'] = message.chat.id
                params['metro_dist'] = 1000
                save_parameters(all_params)
                keyboard = types.InlineKeyboardMarkup()
                button_bar = types.InlineKeyboardButton('Я подписался', callback_data='sub check')
                keyboard.add(button_bar)
                bot.send_message(chat_id=message.chat.id, text="Чтобы получить результаты поиска подпишитесь на канал @FlatoonChat", reply_markup=keyboard)
                
                send_old_ads_tg(message, all_params)
                send_old_ads(message, all_params) 
                activate_test_subscription(message)
                return
            except:
                
              #  import pdb; pdb.set_trace()
                while True:
                    print(123)
                    try:
                        user_data[user_id]  = {
            'model': 'gpt-4o-mini', 
            'messages': [ {'role': 'user', 'content': "{} преобразуй этот json в корректный json, чтобы можно было преобразовать его с помощью json.loads() в python верни мне чистый json без всяких символов потому что я возьму твой response и засуну в json.loads() вот так json.loads(response) так что сделай без всяких лишних символов чистый json !!  ".format(user_data[str(user_id) + "resp"])}
            ]}
                       
                        user_data[user_id]  = json.loads(dialogue(user_data[user_id] ))
                
                        break
                    except:
                        print(traceback.format_exc())
                user_data[user_id]['username'] = message.from_user.username
                user_data[user_id]['chat_id'] = message.chat.id
                user_data[user_id]['metro_dist'] = 1000
                #if user_data[user_id]['sex'] == 
                all_params = load_parameters()
                all_params[str(message.chat.id)] = user_data[user_id]
                save_parameters(all_params)
                keyboard = types.InlineKeyboardMarkup()
                button_bar = types.InlineKeyboardButton('Я подписался', callback_data='sub check')
                keyboard.add(button_bar)
                bot.send_message(chat_id=message.chat.id, text="Чтобы получить результаты поиска подпишитесь на канал @FlatoonChat", reply_markup=keyboard)
                 
                activate_test_subscription(message)
                return
        user_data[user_id]['messages'].append({"role": "assistant", "content":"{}".format(response)})
        bot.send_message(message.chat.id, "{}".format(response))
        bot.register_next_step_handler(message, lambda msg: cont(msg, data_=user_data[user_id]))
    
    @bot.message_handler(func=lambda message: True)
    def start_start(message):
        
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Женщина👩‍🦱 ', callback_data='sex 0')
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Мужчина🤵‍♂️', callback_data='sex 1') 
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Я один', callback_data='sex 2') 
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Нас двое', callback_data='sex 3') 
        keyboard.add(button_bar)
        TINY_DB[message.chat.id]['sex_input'] = [False, False, False, False]
        bot.send_message(message.chat.id, "Для начала выберите ваш пол, даже если вас двое.\n Вы будете получать объявления, в которых собственник ищет людей вашего пола, с учётом вашего количества.\nМожно выбрать несколько.", reply_markup=keyboard)
    
    
    def get_mates(message):
        keyboard = types.InlineKeyboardMarkup()
        
        button_bar2 = types.InlineKeyboardButton('Женщины 👩‍🦱', callback_data='mate 0')
        button_bar = types.InlineKeyboardButton('Мужчины 👨‍🦰', callback_data='mate 1')
        keyboard.add(button_bar2)
        keyboard.add(button_bar)
        
        button_bar = types.InlineKeyboardButton('Один сосед 🤼‍♂️', callback_data='mate 2')
        button_bar2 = types.InlineKeyboardButton('Больше одного соседа 👯‍♂️👯‍♀️', callback_data='mate 3')
        keyboard.add(button_bar)
        keyboard.add(button_bar2)
        TINY_DB[message.chat.id]['mates_input'] = [False, False, False, False]
        bot.send_message(message.chat.id, "Отлично. Кого бы вы хотели видеть в вашх соседях (Это нужно для комнат)?\n" 
                         "Можно выбрать несколько.", reply_markup=keyboard)
        
    def get_rent_period(message):
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Короткий', callback_data='period 0')
        button_bar2 = types.InlineKeyboardButton('Долгий', callback_data='period 1')
        keyboard.add(button_bar)
        keyboard.add(button_bar2)
        TINY_DB[message.chat.id]['period_input'] = [False, False]
        bot.send_message(message.chat.id, "Срок аренды?\n" 
                         "Можно выбрать несколько.", reply_markup=keyboard)
    # Обработка ввода количества комнат
    def get_animal(message):
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Кошка 🐈‍⬛', callback_data='animal 0')
        button_bar2 = types.InlineKeyboardButton('Собака 🦮', callback_data='animal 1')
        
        keyboard.add(button_bar)
        keyboard.add(button_bar2)
        button_bar = types.InlineKeyboardButton('Пропустить', callback_data='animal continue')
        keyboard.add(button_bar)   
        TINY_DB[message.chat.id]['animal_input'] = [False, False]
        bot.send_message(message.chat.id, "Осталось чуть-чуть. Есть ли животные?\n" 
                         "Можно выбрать несколько.", reply_markup=keyboard)
    def old_start(message):
        #TINY_DB[message.chat.id] = {}
        TINY_DB[message.chat.id]['state'] = 'start'
        #save_action( message.chat.id, 'start')
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Комнаты ', callback_data='start 0')
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Однокомнатные квартиры', callback_data='start 1')
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Двухкомнатные квартиры', callback_data='start 2')
        keyboard.add(button_bar)
        button_bar = types.InlineKeyboardButton('Трехкомнатные квартиры', callback_data='start 3')
        keyboard.add(button_bar)
        TINY_DB[message.chat.id]['rooms_input'] = [False, False, False, False]
        
        bot.send_message(message.chat.id, "Что будем искать?", reply_markup=keyboard)
    def get_rooms(message):
        try:
            #TINY_DB[message.chat.id]['state'] = 'get_rooms'
            
            rooms = []
            global TINY_DB
            rooms_input = TINY_DB[message.chat.id]['rooms_input']
            for i in range(len(rooms_input)):
                if rooms_input[i]:
                    rooms.append({'rooms': i, 'min_price': None, 'max_price': None})
            # Сохраняем количество комнат в контексте пользователя
            if rooms[0]['rooms'] == 0:

                bot.send_message(message.chat.id, "Напишите минимальную арендную плату для комнат. (Например: 30000)".format(rooms[0]['rooms']))
            else:
                bot.send_message(message.chat.id, "Напишите минимальную для {}-комнатных вариантов арендную плату. (Например: 30000)".format(rooms[0]['rooms']))
            TINY_DB[message.chat.id]['rooms'] = rooms                                   
            
            bot.register_next_step_handler(message, lambda msg: get_min_price(msg))
        except ValueError:
            print(traceback.format_exc())
            bot.send_message(message.chat.id, "Пожалуйста, введите корректные числа.")

    def get_min_price(message, next_=0, rooms=0):
        try:
            if rooms == 0:
                rooms = iter(TINY_DB[message.chat.id]['rooms'])
            if next_ == 0:
                next_ = next(rooms)
            min_price = int(message.text)
            next_['min_price'] = min_price
            bot.send_message(message.chat.id, "Теперь напишите максимальную арендную плату.")
            bot.register_next_step_handler(message, lambda msg: get_max_price(msg, next_, rooms))
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")

    def get_max_price(message, next_, rooms):
        #save_action(message.chat.id, 'max_price')
        try:
            max_price = int(message.text)
            if max_price < 500:
                max_price = max_price*1000 
            next_['max_price'] = max_price
            try:
                next_ = next(rooms)
                bot.send_message(message.chat.id, "Теперь напишите минимальную арендную плату для {}-комнатных квартир.".format(next_['rooms']))
                bot.register_next_step_handler(message, lambda msg: get_min_price(msg, next_, rooms))
            except:
                keyboard = types.InlineKeyboardMarkup()
                button_bar = types.InlineKeyboardButton('Пропустить', callback_data='undergrounds continue')
                keyboard.add(button_bar)  
                bot.send_message(message.chat.id, "Теперь укажите автономный округ, район или станцию метро с большой буквы, через запятую пример: (Замоскворечье, СЗАО, САО, Маяковская, Алексеевская)", reply_markup=keyboard)
                
                bot.register_next_step_handler(message, lambda msg: get_undergrounds(msg))
        except ValueError:
            print(traceback.format_exc())
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")


    def get_undergrounds(message, skip = False):
        
        global TINY_DB
        if not skip:    
            undergrounds_input = message.text.split(',')
    
            TINY_DB[message.chat.id]['undergrounds'] = [station.strip() for station in undergrounds_input]
            keyboard = types.InlineKeyboardMarkup()
            button_bar = types.InlineKeyboardButton('Да', callback_data='check_under yes')
            keyboard.add(button_bar) 
            
            button_bar = types.InlineKeyboardButton('Ввести заново', callback_data='check_under retry')
            keyboard.add(button_bar)
            bot.send_message(message.chat.id, "Вы ввели следующие параметры: "+ str(TINY_DB[message.chat.id]['undergrounds']), reply_markup=keyboard)
        else :
            TINY_DB[message.chat.id]['undergrounds']=".*"
            
            check_undergrounds(message)
                               
        
    def get_author_type(message, skip = False, author = False):
        global TINY_DB
        
        if not skip and author:
            TINY_DB[message.chat.id]['author_type'] = "Владелец"
        else:
            TINY_DB[message.chat.id]['author_type'] = "Любой"
        
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Пропустить', callback_data='dist continue')
        keyboard.add(button_bar)  
        bot.register_next_step_handler(message, lambda msg: get_metro_dist(msg))
        bot.send_message(message.chat.id, "Теперь укажите максимальное количество минут до метро (например, 10)\n", reply_markup=keyboard)                                 
    
    def check_undergrounds(message, skip = False):
        
        keyboard = types.InlineKeyboardMarkup()
        button_bar = types.InlineKeyboardButton('Да', callback_data='author yes')
        keyboard.add(button_bar) 
        
        button_bar = types.InlineKeyboardButton('Пропустить', callback_data='author continue')
        keyboard.add(button_bar)
        bot.send_message(message.chat.id, "Хотите ли получать предложения только от собственников?\n", reply_markup=keyboard)



    def get_metro_dist(message, skip = False):
       # import pdb; pdb.set_trace()
        TINY_DB[message.chat.id]['period_input'] = ""
        #bot.register_next_step_handler(message, lambda msg: start(msg))
        if not skip:
            TINY_DB[message.chat.id]['metro_dist'] = int(message.text)
        else:
            TINY_DB[message.chat.id]['metro_dist'] = 1000
        subflag = 0
        subsubflag = 0
        all_params = load_parameters()
        try:
            if "test_subscription" in all_params[str(message.chat.id)]:
                subflag = all_params[str(message.chat.id)]["test_subscription"]
            if "subscription" in all_params[str(message.chat.id)]:
                subsubflag = all_params[str(message.chat.id)]["subscription"]
        except:
            print(traceback.format_exc())
            # Сохранение параметров для текущего чата
        all_params[str(message.chat.id)] = {
            'username':TINY_DB[message.chat.id]['username'],
            'rooms': TINY_DB[message.chat.id]['rooms'],
            'undergrounds': TINY_DB[message.chat.id]['undergrounds'],
            'chat_id': message.chat.id,
            'author_type' : TINY_DB[message.chat.id]['author_type'],
            'metro_dist': TINY_DB[message.chat.id]['metro_dist'],
            'sex': TINY_DB[message.chat.id]['sex_input'],
            'animal': TINY_DB[message.chat.id]['animal_input'] ,
            'mates': TINY_DB[message.chat.id]['mates_input'],
            'period': TINY_DB[message.chat.id]['period_input'],
            'initial_price_value':TINY_DB[message.chat.id]['rooms'][0]['max_price'],
             'initial_undergrounds_value':TINY_DB[message.chat.id]['undergrounds']
        }
        if subflag != 0:
            all_params[str(message.chat.id)]["test_subscription"] = subflag
        if subsubflag != 0:
            all_params[str(message.chat.id)]["subscription"] = subsubflag
        #import pdb; pdb.set_trace()
        
        save_parameters(all_params) 
        all_params = load_parameters()
       # import pdb;pdb.set_trace()
        send_old_ads_tg(message, all_params)
        send_old_ads(message, all_params) 
        activate_test_subscription(message)

        
        
    bot.polling(none_stop=True)
               
    #import threading
    #threading.Thread(target=watch_json_file, daemon=True).start()
def send_greeting_ads():
    pass
    # Запуск бота
if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        