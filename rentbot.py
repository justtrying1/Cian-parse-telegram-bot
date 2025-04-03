
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


PARAMS_FILE = r"params.json"
def load_parameters():
    if os.path.exists(PARAMS_FILE):
        with open(PARAMS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}
from ai import a, dialogue


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
bot.polling()