DIALOGUES_FILE = "dialogues.json"
_DIALOGUES_FILE = "_dialogues.json"
import os
import json
def load_dialogues():

    if os.path.exists(DIALOGUES_FILE):
        with open(DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringA = json.load(file)
        with open(_DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringB = json.load(file)
        jsonMerged = jsonStringA | jsonStringB
        return jsonMerged
    return {}



a = load_dialogues()


import pdb; pdb.set_trace()

