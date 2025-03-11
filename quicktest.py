OLD_JSON = r"&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
def load_old():
    while True:
        try:

            with open(OLD_JSON, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass
import json
a = []
b = []
old = load_old()
import pdb; pdb.set_trace()
for i in old:
    for j in old[i]:
        if ("мужч" in j['description']):
            a.append(j)
            
            if 'addon' not in j:
                b.append(j)
                print(j['description'])
print(len(a))
print(len(b))
