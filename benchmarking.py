from ai import chain_prompt
import json
dt = {
'model': 'gpt-4o-mini', 
'messages': [ {'role': 'user', 'content': r"{0} {1}"}]}
try:
    with open("desc_bench_new.json", 'r', encoding='utf-8') as file:
        l = json.load(file)
except:
    l = []
with open("benchmarking.json", 'r', encoding='utf-8') as file:
    desc_json = json.load(file)

for desc in desc_json[100:150]:
    
    desc_prompt, good_desc = chain_prompt(data=dt, desc=desc, type = 1)
    l.append([desc, desc_prompt, good_desc, 0.5])
    dt = {
            'model': 'gpt-4o-mini', 
            'messages': [ {'role': 'user', 'content': r"{0} {1}"}]}  
    
    with open("desc_bench_new.json", "w", encoding='utf-8') as final:
	    json.dump(l, final, ensure_ascii=False)
                     