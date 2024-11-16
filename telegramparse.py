from telethon.sync import TelegramClient
 
import csv
 
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# Введите свои API ID и API Hash
api_id = '10982534'
api_hash = '4b42f67f092c288c4af034e4e98a29eb'

# Создайте объект клиента
client = TelegramClient('session_name', api_id, api_hash)

# Войдите в систему
client.start()

chats = []
last_date = None
size_chats = 200
groups=[]
result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
        ))
chats.extend(result.chats)
for chat in chats:
   try:
       if chat.megagroup== True:
           groups.append(chat)
   except:
       continue
print('Выберите номер группы из перечня:')
i=0
for g in groups:
   print(str(i) + '- ' + g.title)
   i+=1