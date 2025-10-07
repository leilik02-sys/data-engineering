import requests
import json
url = "https://xivapi.com/Action"  # ссылка на api по final fantasy

import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Создаем папку для сохранения JSON 
DATA_DIR = os.path.join(BASE_DIR, "xiv_data") # Место для хранения сырых данных


def setup_dir():
    os.makedirs(DATA_DIR, exist_ok=True)   #Создаём папку для сырых данных JSON
    print("Папка xiv_data готова.\n")


def fetch_action(action_id: int):
    api = f"{url}/{action_id}"  # Делаем запрос к нашему api адресу и возвращаем словарь с данными
    response = requests.get(api)  

    if response.status_code == 200:
        data = response.json()   
        return data
    else:
        print("Ошибка: ({response.status_code}) для ID {action_id}")
        return None


def save_json(item: dict): # Кладём наш ответ в xiv_data
    aid = item.get("ID")
    if aid is None:
        return
    path = os.path.join(DATA_DIR, f"action_{aid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)


def to_dataframe_final_fantasy(records: list[dict]) -> pd.DataFrame:  # Преобразуем список JSON-объектов из api в DataFrame
    if not records:
        return pd.DataFrame()


    df = pd.json_normalize(records, sep=".")  # Изменяем вложенные поля в формат ClassJob.NameEnglish


    for col in [c for c in df.columns if c.startswith("Description")]:      # Очищаем HTML-теги из описаний
        df[col] = df[col].astype(str).str.replace(r"<[^>]+>", "", regex=True)

    # Если в колонке есть список, то нужно распаковать его в отдельные строки
    list_cols = [c for c in df.columns if df[c].apply(lambda x: isinstance(x, list)).any()]
    for col in list_cols:
        df = df.explode(col, ignore_index=True)

    # Если в колонке есть словарь, то нужно развернуть его подколонки 
    dict_cols = [c for c in df.columns if df[c].apply(lambda x: isinstance(x, dict)).any()]
    for col in dict_cols:
        sub = pd.json_normalize(df[col].dropna().tolist(), sep=".")
        sub.index = df[col].dropna().index
        sub = sub.add_prefix(f"{col}.")
        df = df.drop(columns=[col]).join(sub, how="left")

  
    keep = [   # Выбираем нужные нам поля
        "ID", "Name", "Name_en", "Name_ja", 
        "Description", "Description_en",
        "Icon", "IconHD",
        "ClassJob.ID", "ClassJob.NameEnglish",
        "Cast100ms", "Recast100ms", "Range", "EffectRange", "CooldownGroup"
    ]
    cols = [c for c in keep if c in df.columns]
    return df[cols] if cols else df


def download_actions(ids: list[int]): # Загружаем данные по указанным ID и сохраняем их
    
    setup_dir() # Подготавливаем папку для сохранения JSON 
    collected = []  # Создаём пустой список, куда будем складывать все ответы API
    for aid in ids:  # Проходимся по каждому ID из списка
        item = fetch_action(aid)  # Получаем JSON по конкретному ID
        if not item:
            continue
        save_json(item) # Сохраняем полученный JSON в файл xiv_data
        collected.append(item) # Добавляем словарь в общий список
    return collected # Возвращаем список всех загруженных JSON-объектов


if __name__ == "__main__":
    ids = [127, 16, 27] # Возьмем для примера три разных умения 

    result = download_actions(ids) # Загружаем данные

    df = to_dataframe_final_fantasy(result)  # Преобразуем JSON в DataFrame

    # Чтобы таблица выглядела аккуратно
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)
    pd.set_option("display.max_colwidth", 80)

    # Отбираем ключевые поля для печати
    use = [c for c in [
        "ID", "Name_en", "Name_ja", "Name", 
        "Description_en", "ClassJob.NameEnglish",
        "Cast100ms", "Recast100ms", "Range", "EffectRange", "CooldownGroup"
    ] if c in df.columns]

    print("Размер таблицы:", df.shape)
    print("Колонки:", ", ".join(use))
    print("\nПервые строки (ключевые поля):")
    print(df[use].head().to_string(index=False))