OLD_JSON = r"&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
import json
import traceback
def load_old():
    while True:
        try:

            with open(OLD_JSON, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            
            print(traceback.format_exc())
old = load_old()
for i in old:
    old[i] = old[i][-100:]
while True:
        try:
            print(3)
            with open(OLD_JSON, "w", encoding='utf-8') as new_file:       
                json.dump(old, new_file, ensure_ascii=False, indent = 6)
            break
        except:
            import traceback
            print(traceback.format_exc())