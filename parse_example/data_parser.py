import os
import json
import datetime
import requests
from bs4 import BeautifulSoup


url = "https://www.rbc.ru/economics/"  # Сайт с новостями РБК, раздел "Экономика"


def build_headers(): # Создаём заголовки для запроса
    
    headers = {
         "User-Agent": "Mozilla/5.0",   # Представляемся как обычный браузер, чтобы сайт не блокировал запрос
        "Accept": "text/html"   # Запрашиваем HTML-страницу
    }
    return headers


def fetch_html(url):  # Получаем HTML страницы
   
    headers = build_headers()
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
        else:
            print("Ошибка при подключении:", response.status_code)
            html = ""
    except Exception as e:
        print("Произошла ошибка при запросе:", e)
        html = ""
    return html


def extract_articles(html): # Находим статьи и сохраняем в словарь
    
    articles_dict = {}

    if html == "":
        print("HTML пустой, нечего парсить.")
        return articles_dict

    soup = BeautifulSoup(html, "lxml")

    # Пробуем найти статьи по разным классам
    articles = soup.find_all("a", class_="item__link")
    if len(articles) == 0:
        articles = soup.find_all("a", class_="news-feed__item")

    for article in articles:
        title = article.get_text(strip=True)
        link = article.get("href")

        if title and link and "rbc.ru" in link:
            articles_dict[title] = link

    return articles_dict


def save_json(data):  # Сохраняем словарь с новостями в JSON
   
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    # Проверяем, существует ли папка, если нет — создаём
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filename = f"rbc_articles_{datetime.date.today().strftime('%d_%m_%Y')}.json"
    file_path = os.path.join(data_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Файл успешно сохранён:", file_path)
    except Exception as e:
        print("Ошибка при сохранении:", e)


def parse_rbc_section(): # Основная функция, которая скачивает страницу, находит статьи и сохраняет их в файл
    
    print("Скачиваем страницу")
    html = fetch_html(url)
    print("Извлекаем статьи")
    articles = extract_articles(html)
    print("Найдено статей:", len(articles))

    if len(articles) > 0:
        save_json(articles)
        print("\n Парсер завершил работу успешно. Новости сохранены")
    else:
        print("Нет статей для сохранения")
        
parse_rbc_section()
