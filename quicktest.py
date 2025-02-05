import re 
print(list(filter(re.compile ("Маяковская".lower()).match, list(map(lambda x: x.lower(), ["Маяковская"])))))
print(re.split(r",\s+", "123, 123, 123", maxsplit=100))