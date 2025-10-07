from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import datetime
import json
import os

url = "https://www.rbc.ru/economics/"  # URL сайта раздела "Экономика"

ua = UserAgent()  # Создаём user-agent
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": ua.google,
}

response = requests.get(url, headers=headers)  # Получаем HTML страницы
if response.status_code == 200:
    html = response.text
else:
    print(f"Ошибка при подключении: {response.status_code}")
    html = ""

soup = BeautifulSoup(html, "lxml")  # Парсим страницу с помощью BeautifulSoup

articles = soup.find_all("a", class_="item__link") or soup.find_all(
    "a", class_="news-feed__item"
)  # Ищем карточки новостей

article_dict = {}  # Создаём словарь с результатами

for article in articles:
    title = article.get_text(strip=True)
    link = article.get("href")
    if title and link and "rbc.ru" in link:
        article_dict[title] = link

# Определяем путь к директории parse_example
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Путь к текущему файлу
DATA_DIR = os.path.join(BASE_DIR)  # Сохраняем в ту же папку, где лежит скрипт

filename = os.path.join(  # Создаём имя файла с датой
    DATA_DIR, f"rbc_articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json"
)

with open(filename, "w", encoding="utf-8") as f:
    try:
        json.dump(article_dict, f, indent=4, ensure_ascii=False)
        print(f" Новости успешно сохранены в файл {filename}")
        print(f" Всего новостей собрано: {len(article_dict)}")
    except Exception as e:
        print(f" Ошибка при сохранении: {e}")
