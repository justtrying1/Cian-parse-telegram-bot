from telegrambot import parse_addon
import json
from telegrambot import load_parameters
params = load_parameters()
#import pdb;pdb.set_trace()
params = params['781665670']
params['undergrounds'] = [".*"]
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
                  "post_id": "norealtor/10302",
                  "text": "\nХАТА СНЯТА | Аренда жилья Москва | Снять квартиру\nСдам квартиру-студию 27м2М. Нижегородская, ул. Газгольдерная д. 1043 000 руб/мес — МаринаCдaeтcя квaртирa -студия  комфорт-клaсcа ЖK Profit c евpоpeмoнтoм. Kвaртира не укoмплектовaна дo конца, поэтому цена на пepвый мeсяц 43 000, далee 55 000. Прeдложeниe oт coбcтвенника, без комиccий.Удoбное траcпoртное pаcпoлoжение м. Hижегоpодcкaя, БКЛ , MЦД-4 . Развитая инфраструктура , аптеки , магазины, ТЦ. Показ квартиры по предварительной договоренности: 18 и 19 февраля.Без животных.Агентам прошу не беспокоить.#недорогаяхата\n2.8K views21:19\n",
                  "link": "https://t.me/norealtor/10302?single",
                  "addon": [
                        {
                              "классификация объявления": "сдача студии",
                              "сколько людей живёт в настоящий момент в квартире?": "не указано",
                              "стоимость месячной аренды": 43000,
                              "стоимость залога/комиссии": "не указано",
                              "кто живёт в настоящий момент": {
                                    "никто": []
                              },
                              "характер ограничения": "не указано",
                              "можно ли заселиться с животными": "нет",
                              "изолированная ли комната": "не указано",
                              "сколько комнат в квартире": "не указано",
                              "ищут ли одного человека": "не указано",
                              "ищут ли двух человек": "не указано",
                              "ищут ли одну женщину/девушку": "не указано",
                              "ищут ли одного мужчину/парня": "не указано",
                              "ищут ли пару из мужчины и женщины": "не указано",
                              "ищут ли пару женщин/девушек": "не указано",
                              "ищут ли пару мужчин/парней": "не указано",
                              "сколько людей живет в настоящий момент в квартире": 0
                        }
                  ],
                  "good_description": "Классификация объявления: сдача студии\n\nКого ищут: не указано  \nНа какой срок: не указано  \nМожно с животными: нет  \nКто живет в квартире: не указано  \nМетро: м. Нижегородская  \nРасстояние до метро: не указано  \nЗалог: не указано  \nСтоимость месячной аренды: первый месяц 43 000 руб, далее 55 000 руб  "
            }
                  ]
                  
import pdb;
pdb.set_trace()
from telegrambot import filter_ads_tg, send_old_ads, load_ads, filter_ads
from datetime import datetime

dont_flag = True
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
            print(msg)
            count = count + 1 
            do_flag = True
      if count > 3 or (datetime.strptime(ad['time'], '%Y-%m-%d  %H-%M-%S') - datetime.now()).days > 10:
            break
if do_flag:
      
      print(132)
else:
      dont_flag = dont_flag + 1
      if dont_flag > 0:   
            params['author_type'] = "Любой"
      if dont_flag > 1:
            params['rooms'][0]['max_price'] = params['rooms'][0]['max_price'] + 2500
      if dont_flag > 3:
            params['undergrounds'] = ".*"
      if dont_flag > 4:
            print(132)
      