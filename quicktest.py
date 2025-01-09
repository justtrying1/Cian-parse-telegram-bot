<<<<<<< Updated upstream
print("не" in "не указано")
=======
import datetime 
b = datetime.datetime(2024, 11, 30, 3,28,45)
#print(b.replace(day=b.day+))
a = str(b+datetime.timedelta(days=3))
c = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
print(str(b+datetime.timedelta(days=3) ))
print((c - datetime.datetime.now()).total_seconds())
print((b - datetime.datetime.now()))
>>>>>>> Stashed changes
