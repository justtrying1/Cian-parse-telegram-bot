DIALOGUES_FILE = "dialogues.json"
_DIALOGUES_FILE = "_dialogues.json"
import os
import json
def load_dialogues():

    if os.path.exists(DIALOGUES_FILE):
        with open(DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringA = json.load(file)
        with open(_DIALOGUES_FILE, 'r', encoding='utf-8') as file:
            jsonStringB = json.load(file)
        jsonMerged = jsonStringA | jsonStringB
        return jsonMerged
    return {}



a = load_dialogues()

import requests
from bs4 import BeautifulSoup

def get_moscow_metro_stations():
    url = "https://ru.wikipedia.org/wiki/Список_станций_Московского_метрополитена"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    stations = []
    
    # Находим все таблицы с классами 'standard' или 'wikitable'
    tables = soup.find_all('table', {'class': ['standard', 'wikitable']})
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Пропускаем заголовок
            cols = row.find_all('td')
            if cols:
                station_name = cols[0].get_text(strip=True)
                # Убираем сноски и лишние символы
                station_name = station_name.split('[')[0].strip()
                stations.append(station_name)
    
    return sorted(list(set(stations)))  # Убираем дубликаты и сортируем

if __name__ == "__main__":
    stations = get_moscow_metro_stations()
    print(f"Всего станций: {len(stations)}")
    for station in stations:
        print(station)
import pdb; pdb.set_trace()

