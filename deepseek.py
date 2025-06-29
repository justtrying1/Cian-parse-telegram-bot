# Please install OpenAI SDK first: `pip3 install openai`

#from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import traceback
load_dotenv()
import requests
api_key = os.environ.get("DEEPSEEK_API_KEY")

cian = "Привет, ты представитель арендатора, который хочет себе снять квартиру, ты должен представить своего клиента, а также назначить встречу.  Я буду использовать твои ответы для автоматического диалога с арендодателем.  Отвечай таким образом чтобы твое сообщение можно было бы сразу переслать, то есть без всяких лишних символов. (Ты буквально разговариваешь с ним, потому что я пересылаю ему твои сообщения!) Если у клиента есть животное постарайся убедить риелтора в возможности проживания с животным. Назначай встречу в самую последнюю очередь (после того как узнаешь можно ли с животными и можно ли нашему жильцу жить в квартире). Если арендодатель хочет назначить встречу, верни в качестве ответа текст со значением 'vstrecha vstrecha' Общайся от имени представителя не от имени потенциального квартиро-съемщика.  Не здоровайся! Если тебе предлагают перейти в мессенджер или позвонить по телефону, отвечай, что тебе удобнее общаться здесь, Ты должен общаться только в рамках чата и сообщать собесденику, что ты не готов переходить ни в какие стороние мессенджеры в целях безопасности. Если сообщения повторяются несколько раз и ты чувствуешь что диалог зашел в тупик , и ты уже оставил свое предложение (представил клиента), в таком случае верни мне текст 'robot vs robot', если встреча была назначена, у тебя есть номер телефона риелтора и диалог пришел к логическому завершению, то верни текст 'vstrecha set (далее текст по типу: Встреча назначена на такое то число такое то время, и верни контакты риелтора)' "
#cian = "Привет"
data_ = {
    'model': 'deepseek-reasoner', 
    'messages': [ {'role': 'user', 'content': r"{0}{1}"}
                  ] }       
    
url = "https://api.deepseek.com/chat/completions"
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

#response = requests.post(url, headers=headers, data=json.dumps(data_))

def dialogue(data=data_, desc = ""):
    data['messages'][0]['content'] = data['messages'][0]['content'].format("Вот описание клиента: {}\n".format(desc), cian)
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            break
    #print(data['messages'][0]['content'])
        except:
            
            print(traceback.format_exc())
    # Проверка статуса ответа
    if response.status_code == 200:
        # Парсинг JSON-ответа
        response_data = response.json()
        #print(response_data['choices'][0]['message']['content'])
        return(response_data['choices'][0]['message']['content'])
    else:
        print(f'Ошибка: {response.status_code}, {response.text}')
#
def aliluya():
    import pdb; pdb.set_trace()
    #response = dialogue(data_ )
    data_['messages'].append({"role": "assistant", "content":"{}".format("Здравствуйте. Уточните, пожалуйста, ещё сдаёте?")})
    while True:
        
        data_['messages'].append({"role":"user", "content":"{}".format(input())})
        response = dialogue(data_ )
        data_['messages'].append({"role": "assistant", "content":"{}".format(response)})
if __name__ == "__main__":
    aliluya()