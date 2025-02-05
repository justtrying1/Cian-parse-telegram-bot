import re 
print(list(filter(re.compile ("".lower()).match, list(map(lambda x: x.lower(), ["Маяковская"])))))
print(re.split(r",\s+", "123, 123, 123", maxsplit=100))
for i in [1,2,3,4,][::-1]:
    print (i)
if False:
    pass
elif False:
    print(123123)