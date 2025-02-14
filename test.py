from telegrambot import parse_addon
import json
from telegrambot import load_parameters
params = load_parameters()
#import pdb;pdb.set_trace()
params = params['7494874190']
params['undergrounds'] = ["Останкинский"]
#with open("desc_bench_new.json", "r", encoding='utf-8') as final:
    #loaded = json.load(final)
"""
for i in loaded[25:]:
    
    addon = i[1][0]
    #if any("человек" in a for a in addon['тип разыскиваемого жильца']) or addon['ищут ли семейную пару'] == 'да':
    
    d = []
    
    try:
            
            print(111111111111)
            print(i)
            a = parse_addon(i[1], params)
            print(a)
            print(i[0])
            #d.append(i[1])
    except:
        pass       
 
    #for j in i[1]:
    #    print(j)
        #parse_addon()
        """
addon = [{'сколько людей живёт в настоящий момент в квартире?': 0, 'кто живёт в настоящий момент': {'никто': []}, 'характер ограничения': 'строго', 'можно ли заселиться с животными': 'нет', 'изолированная ли комната': 'не указано', 'сколько комнат в квартире': 2, 'ищут ли одного человека': 'нет', 'ищут ли двух человек': 'нет', 'ищут ли одну женщину/девушку': 'да', 'ищут ли одного мужчину/парня': 'нет', 'ищут ли пару из мужчины и женщины': 'нет', 'ищут ли пару женщин/девушек': 'не указано', 'ищут ли пару мужчин/парней': 'нет'}]
addon =  [
                        {
                              "сколько людей живёт в настоящий момент в квартире?": 1,
                              "кто живёт в настоящий момент": {
                                    "студент": [
                                          "мужчина",
                                          20
                                    ]
                              },
                              "характер ограничения": "не указано",
                              "можно ли заселиться с животными": "не указано",
                              "изолированная ли комната": "да",
                              "сколько комнат в квартире": 3,
                              "ищут ли одного человека": "не указано",
                              "ищут ли двух человек": "не указано",
                              "ищут ли одну женщину/девушку": "не указано",
                              "ищут ли одного мужчину/парня": "не указано",
                              "ищут ли пару из мужчины и женщины": "не указано",
                              "ищут ли пару женщин/девушек": "не указано",
                              "ищут ли пару мужчин/парней": "не указано"
                        }
                  ]
                  
import pdb;
pdb.set_trace()
from telegrambot import filter_ads
a = filter_ads([{"author": "ID 23864095",
                  "author_type": "Владелец",
                  "floor": 2,
                  "floors_count": 5,
                  "rooms_count": 0,
                  "total_meters": 10.0,
                  "price_per_month": 22000,
                  "commissions": 0,
                  "district": "Останкинский",
                  "street": "2-я Новоостанкинская ",
                  "house_number": "23",
                  "underground": "Улица Академика Королёва",
                  "preload": 0,
                  "metro_dist": "9 минут пешком",
                  "title": "1 комната, 10 м², 2/5 этаж",
                  "description": "Сдаётся комната девушке на долгосрочный период, без вредных привычек.Рабочая неделя 5/2 платежеспособная Проживание с хозяйкой. Сдача жилья от хозяйки, посредников не беспокоить.",
                  "url": "https://www.cian.ru/rent/flat/312136867/",
                  "time": "2025-01-10 16-17-48",
                  "image0": "https://images.cdn-cian.ru/images/komnata-moskva-2ya-novoostankinskaya-ulica-2369562719-4.jpg",
                  "image1": "https://images.cdn-cian.ru/images/komnata-moskva-2ya-novoostankinskaya-ulica-2369557837-4.jpg",
                  "image2": "https://images.cdn-cian.ru/images/komnata-moskva-2ya-novoostankinskaya-ulica-2369557839-4.jpg",
                  "image3": "data:image/svg+xml,%3csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3e%3cpath fill-rule='evenodd' clip-rule='evenodd' d='M2 6 7.707.293l1.414 1.414L4.828 6l4.293 4.293-1.414 1.414L2 6Z' fill='currentColor'/%3e%3c/svg%3e",
                  "image4": "data:image/svg+xml,%3csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3e%3cpath fill-rule='evenodd' clip-rule='evenodd' d='M4.293.293 10 6l-5.707 5.707-1.414-1.414L7.172 6 2.879 1.707 4.293.293Z' fill='currentColor'/%3e%3c/svg%3e",
                  "addon": [
                        {
                              "сколько людей живёт в настоящий момент в квартире": 1,
                              "кто живёт в настоящий момент": {
                                    "хозяйка": [
                                          "женщина",
                                          "не указано"
                                    ]
                              },
                              "характер ограничения": "строго",
                              "можно ли заселиться с животными": "не указано",
                              "изолированная ли комната": "не указано",
                              "сколько комнат в квартире": "не указано",
                              "ищут ли одного человека": "да",
                              "ищут ли двух человек": "нет",
                              "ищут ли одну женщину/девушку": "да",
                              "ищут ли одного мужчину/парня": "нет",
                              "ищут ли пару из мужчины и женщины": "нет",
                              "ищут ли пару женщин/девушек": "нет",
                              "ищут ли пару мужчин/парней": "нет",
                              "сколько людей живёт в настоящий момент в квартире?": 1
                        }
                  ],
                  "good_description": "Кого ищут: девушку  \nСрок: долгосрочный  \nМожно с животными: не указано  \nКто живёт в квартире: хозяйка"
            }], params)
print(parse_addon(a[0]['addon'], params, "good_description"))
print(params)
print(a)