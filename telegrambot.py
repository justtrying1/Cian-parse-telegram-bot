
API_TOKEN = '7006315291:AAE_Nb6L-pNyVi5tFylMycjZnkAYrkkzyYs'  # Замените на ваш токен
JSON_FILE_PATH = '&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json'
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

#API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)


# Путь к локальному JSON-файлу
#JSON_FILE_PATH = 'ads.json'  # Укажите путь к вашему локальному JSON-файлу
last_ads = set()  # Используем множество для хранения уникальных URL объявлений
PARAMS_FILE = "params.json"
CACHE_FILE = "cache.json"
ACTION_FILE = "action"
ACTION_FILE = "{ACTION_FILE}{date}.json".format(ACTION_FILE=ACTION_FILE, date=datetime.now().strftime('%Y-%m-%d %H-%M'))
def load_action():
    try:
        if os.path.exists(ACTION_FILE):
            with open(ACTION_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}
    except:
        return {}
    

def save_action(chat_id, action_name):
    #import pdb; pdb.set_trace()
    action = load_action()
    if str(chat_id) not in action.keys():
        action[str(chat_id)] = {}
    action[str(chat_id)][datetime.now().strftime('%Y-%m-%d %H-%M-%S')] = action_name
    
    with open(ACTION_FILE, 'w', encoding='utf-8') as file:
        json.dump(action, file, ensure_ascii=False)
    
def load_cache():
    with open(CACHE_FILE, "r", encoding='utf-8') as file:
       a = json.load(file)
    return a

def save_cache(appeared):
    
    
    print(len(appeared))
    all_params = load_parameters()
    sent_list = {}
    cache = load_cache()
    for i in all_params.keys():
        chat_id = all_params.get(i)['chat_id']
        new_filtered_ads = filter_ads(appeared, all_params.get(i))
        sent_list[chat_id] = str(len(new_filtered_ads))
        print(str(len(new_filtered_ads)) + "длина появившихся")
        if str(chat_id) not in cache.keys():
            cache[str(chat_id)] = {}
        print(i)
        try:
            if isinstance(cache[str(chat_id)]['last 20'], list):
                cache[str(chat_id)]['last 20'] = {}
        except:
            pass
        if 'last 20' in cache[str(chat_id)].keys():
            pass
        else:
            cache[str(chat_id)]['last 20'] = {}
        if len(cache[str(chat_id)]['last 20'].keys()) > 20:
            for i in list(cache[str(chat_id)]['last 20'].keys())[:-20]:
                cache[str(chat_id)]['last 20'].pop(i)
        if(len(new_filtered_ads)) > 0:
             
           # import pdb; pdb.set_trace()            
            
            try:
              #  import pdb; pdb.set_trace()
                for ad in new_filtered_ads:
                    cache[str(chat_id)]['last 20'][ad['url']] = ad['description']  
                    
                    time_ = datetime.strptime(ad['time'], '%Y-%m-%d %H-%M-%S')
                    button_bar = types.InlineKeyboardButton('Показать описание', callback_data='{}'.format(ad['url']))
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(button_bar)
                    msg = f"""Актуально на {time_}\n"
                                        "{ad['title']}"
                                        "🚇Метро: {ad['underground']} {ad['metro_dist']}\n"
                                        "🧍‍♂️Автор: {ad['author_type']}\n"
                                        "💸Цена: {ad['price_per_month']}₽\n"
                                        "🏘Район: {ad['district']}\n"
                                        "🛏Количество комнат: {ad.get('rooms_count', 'не указано')}\n"
                                        "🔗Источник: {ad['url']}\n"
                                        """
                    if 'addon' in ad:
                        for i in ad['addon'][0]:
                            try:
                                import pdb; pdb.set_trace()
                                if "параметры проживающих" in i:
                                    for j in ad['addon'][0][i]:
                                        for d in ad['addon'][0][i][j]:
                                            if "не указано" not in d:
                                                
                                                msg.append({f"Жилец {j}": ",".join(str(element) for element in ad['addon'][0][i][j])})
                                if "не указано" not in str(ad['addon'][0][i]):
                                    msg.append(f"{i}: {ad['addon'][0][i]}\n")
                            except Exception as e:
                                print(e)
    
                    bot.send_message(chat_id, msg, reply_markup=keyboard)
                bot.send_message(chat_id, text='Появилось {} новых объявления по вашему запросу, чтобы поменять параметры воспользуйтесь командой /start\n'    
                                 "@KvartiraDar - канал про обновления".format(str(len(new_filtered_ads))))
            except:
                print("blocked")
                pass
            save_action("sent", sent_list)
        while True:
            try:
                with open(CACHE_FILE, "w+", encoding='utf-8') as file:
                    json.dump(cache, file, ensure_ascii=False)
                break
            except:
                pass
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
def load_ads():
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для фильтрации объявлений по цене и количеству комнат
def filter_ads(ads, criteria):
    filtered = []

    for ad in ads:       
        for room_criteria in criteria['rooms']:
            try:
                print(criteria['metro_dist'])
            except KeyError:
                criteria['metro_dist'] = 1000
            try:
                print(criteria['author_type'])
            except KeyError:
                criteria['author_type'] = "Любой"
            metro_dist = int(ad['metro_dist'].split(" ")[0])
            try:
                if criteria['author_type'] == "Владелец" and ad['author_type'] == "Владелец":
                    try:
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and list(filter(re.compile ( criteria['undergrounds'] ).match, ad['underground']))):
                            filtered.append(ad)
                    except:    
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and
                            (list(filter(re.compile(ad['underground']).match, criteria['undergrounds'])))):
                        
                                filtered.append(ad)
                elif criteria['author_type'] != "Владелец":
                    try:
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and list(filter(re.compile ( criteria['undergrounds'] ).match, ad['underground']))):
                            filtered.append(ad)
                    except:    
                        if (metro_dist < criteria['metro_dist'] and room_criteria['min_price'] <= ad['price_per_month'] <= room_criteria['max_price'] and
                            ad['rooms_count'] == room_criteria['rooms'] and
                            (list(filter(re.compile(ad['underground']).match, criteria['undergrounds'])))):
                        
                                filtered.append(ad)
                elif criteria['author_type'] == "Владелец" and ad['author_type'] != "Владелец":
                    break
            except KeyError:
                pass        
    return filtered



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
    # import pdb; pdb.set_trace()
        
        if "cian.ru" in call.data:
            try:
                save_action(call.message.chat.id, 'desc')
                print(call.message.chat.id)
                #import pdb; pdb.set_trace()
                a = load_cache()
                msg = bot.send_message(call.message.chat.id, f"📔📔 Описание\n {a[str(call.message.chat.id)]['last 20'][call.data]}", reply_to_message_id=call.message.id)
                bot.pin_chat_message(chat_id=msg.chat.id, message_id=msg.message_id)
            except:
                pass
            
        # button_foo = types.InlineKeyboardButton('Показать новые', callback_data='new')

    @bot.message_handler(commands=['start'])
    def start(message):
        save_action( message.chat.id, 'start')
        bot.send_message(message.chat.id, "Привет! Я бот для уведомления о новых объявлениях об аренде недвижимости. "
                                        "Напишите количество комнат интересующей вас квартиры (или несколько через запятую, \n"
                                        "например: 0,1,2)\n"
                                        "0 - команты, 1 - однокомнатные и т.д.")

    # Обработка ввода количества комнат
    @bot.message_handler(func=lambda message: True)
    def get_rooms(message):
        try:
            rooms_input = message.text.split(',')
            rooms = []
            
            for room in rooms_input:
                room = room.strip()
                rooms.append({'rooms': int(room), 'min_price': None, 'max_price': None})
            
            # Сохраняем количество комнат в контексте пользователя
            bot.send_message(message.chat.id, "Напишите минимальную арендную плату для {}-комантных квартир. (Например: 30000)".format(rooms[0]['rooms']))
                                                
            rooms_copy = []
            bot.register_next_step_handler(message, lambda msg: get_min_price(msg, rooms, rooms_copy))
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректные числа.")

    def get_min_price(message, rooms, rooms_copy):
        try:
            min_price = int(message.text)
            
            rooms[0]['min_price'] = min_price
            bot.send_message(message.chat.id, "Теперь напишите максимальную арендную плату.")
            bot.register_next_step_handler(message, lambda msg: get_max_price(msg, rooms, rooms_copy))
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")

    def get_max_price(message, rooms, rooms_copy):
        save_action(message.chat.id, 'max_price')
        try:
            max_price = int(message.text)
            if max_price < 500:
                max_price = max_price*1000 
            rooms[0]['max_price'] = max_price
            rooms_copy.append(rooms[0])
            if len(rooms) > 1:
                # Переход к следующему количеству комнат
                
                rooms.pop(0)  # Убираем первый элемент из списка
                bot.send_message(message.chat.id, "Теперь напишите минимальную арендную плату для {}-комнатных квартир.".format(rooms[0]['rooms']))
                bot.register_next_step_handler(message, lambda msg: get_min_price(msg, rooms, rooms_copy))
            else:
                # Все варианты обработаны
                bot.send_message(message.chat.id, "Теперь укажите станцию метро с большой буквы (или несколько через запятую, также с большой буквы)."
                                "Или напишите 'пропустить'")
                bot.register_next_step_handler(message, lambda msg: get_undergrounds(msg, rooms_copy))
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")


    def get_undergrounds(message, rooms_copy):
        
        undergrounds_input = message.text.split(',')
        undergrounds = [station.strip() for station in undergrounds_input]
        if (message.text.lower() == "пропустить"):
            undergrounds=".*"
        # Сохраняем все введенные данные
    
        
        # Теперь можно использовать criteria для фильтрации объявлений
        # Например: filtered_ads = filter_ads(all_ads, criteria)
        
        bot.send_message(message.chat.id, "Теперь напишите 'да', если хотите получать предложения только от собственников\n"
                                "А если не хотите, то напишите 'пропустить'")
        bot.register_next_step_handler(message, lambda msg: get_author_type(msg, rooms_copy, undergrounds))
        
    def get_author_type(message, rooms_copy, undergrounds):
        
        if message.text.lower() == "да":
            author_type = "Владелец"
        else:
            author_type = "Любой"
        bot.send_message(message.chat.id, "Теперь укажите максимальное количество минут до метро (например, 10)\n"
                                "А если не хотите, то напишите 'пропустить'")
        bot.register_next_step_handler(message, lambda msg: get_metro_dist(msg, rooms_copy, undergrounds, author_type))
        
        
        
        
    

    def get_metro_dist(message, rooms_copy, undergrounds, author_type):
        try:
            metro_dist = int(message.text)
        except:
            metro_dist = 1000
        all_params = load_parameters()
        
            # Сохранение параметров для текущего чата
        all_params[str(message.chat.id)] = {
            'rooms': rooms_copy,
            'undergrounds': undergrounds,
            'chat_id': message.chat.id,
            'author_type' : author_type,
            'metro_dist': metro_dist
        }
        save_parameters(all_params)  
        
        
        bot.send_message(message.chat.id, "Ваши параметры сохранены. Я буду уведомлять вас о новых объявлениях.")
    bot.polling(none_stop=True)
                        
    #import threading
    #threading.Thread(target=watch_json_file, daemon=True).start()


    # Запуск бота
if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        