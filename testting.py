import json
ddd ="123123123.json"
ccc = "&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
ddd = "actions.json"
import os
PARAMS_FILE = "params.json"
def load_parameters():
    if os.path.exists(PARAMS_FILE):
        with open(PARAMS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def load_old():
    while True:
        try:

            with open(ddd, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass
a = load_old()
all_params = load_parameters()
l = []
for i in a['sent']:
    #for j in all_params.keys():
        #if j in a['sent'][i]:
    print(a['sent'][i].keys())
    l = l + (list(a['sent'][i].keys()))
print(len(set(l)))
print(set(l))
print(set(l) - set(all_params.keys()))
b = set(l) - set(all_params.keys())

print(len(b))
for bb in b:
    if bb not in all_params:
        all_params[str(bb)] = {}
with open(PARAMS_FILE, "w", encoding='utf-8') as new_file:       
    json.dump(all_params, new_file, ensure_ascii=False, indent = 6)