from ai import chain_prompt
from ai import data, desc
ad = chain_prompt(data=data, desc=desc)

a = []
for i in ad[0]:
    try:
       #import pdb; pdb.set_trace()
        if "параметры проживающих" in i:
            for j in ad[0][i]:
                for d in ad[0][i][j]:
                    if "не указано" not in d:
                        
                        a.append({f"Жилец {j}": ",".join(str(element) for element in ad[0][i][j])})
        if "не указано" not in str(ad[0][i]):
            a.append(f"{i}: {ad[0][i]}\n")
    except Exception as e:
        print(e)
print(a)

