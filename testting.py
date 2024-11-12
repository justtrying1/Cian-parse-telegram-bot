import json
ddd ="123123123.json"
ccc = "&rent&30000&40000&1 room&Москва&2024-09-30 22-40-46.json"
def load_old():
    while True:
        try:

            with open(ddd, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass
a = load_old()
l = []
for i in range(5,16):
    for j in a[str(i)]:
        if j['rooms_count'] == 0:
            try:
                l.append(j['description'])
            except:
                pass
print(len(l))
print(len(set(l)))


# File name is mydata.json
with open("benchmarking.json", "w", encoding='utf-8') as final:
	json.dump(list(set(l)), final, ensure_ascii=False)
