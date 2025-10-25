import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import os
import sqlite3

# Получение параметров подключения к базе данных

def get_connection_settings(db_file="creds.db"):
    """
    Извлекает учётные данные PostgreSQL из локальной базы creds.db.
    В таблице access должны быть поля: url, port, user, pass.
    """
    try:
        # Открываем соединение с SQLite-базой
        conn = sqlite3.connect(db_file)
        
        # Читаем первую строку таблицы access
        settings_data = pd.read_sql_query(
            "SELECT url, port, user, pass FROM access LIMIT 1", conn
        )
        
        # Закрываем соединение
        conn.close()
        
        # Преобразуем результат в словарь
        return settings_data.iloc[0].to_dict()
    
    except Exception as e:
        print(f"Ошибка при чтении {db_file}: {e}")
        return None


# Загрузка данных из parquet или Google Drive
def load_data():
   
    try:
        # Проверяем, есть ли локальный файл parquet
        if os.path.exists("Data_clean.parquet"):
            print("Файл Data_clean.parquet найден — загружаем его.")
            df = pd.read_parquet("Data_clean.parquet")
            print(f"Загружено {len(df)} строк из очищенного файла.")
            return df

        # Если parquet нет — загружаем CSV с Google Drive
        print("Файл Data_clean.parquet не найден. Загружаем CSV из Google Drive...")
        FILE_ID = "14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X"
        file_url = f"https://drive.google.com/uc?id={FILE_ID}"
        df = pd.read_csv(file_url)
        print(f"Исходный CSV загружен ({len(df)} строк).")

        # Приведение типов
        print("Приведение типов данных...")
        if "year" in df.columns:
            df["year"] = pd.to_datetime(df["year"].astype(str), format="%Y", errors="coerce")
        if "population" in df.columns:
            df["population"] = pd.to_numeric(df["population"], errors="coerce").astype("Int64")
        for col in ["iso_code", "Name", "Description"]:
            if col in df.columns:
                df[col] = df[col].astype("category")

        # Сохраняем результат в parquet
        df.to_parquet("Data_clean.parquet", index=False)
        print("Файл Data_clean.parquet создан и сохранён локально.")
        return df

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None


# Загрузка данных в PostgreSQL

def upload_to_database(df, db_settings, db_name, table_name):
    
   # Подключается к PostgreSQL и записывает данные в таблицу public.<table_name>.
    try:
        # Формируем строку подключения
        conn_string = (
            f"postgresql+psycopg2://{db_settings['user']}:{db_settings['pass']}"
            f"@{db_settings['url']}:{db_settings['port']}/{db_name}"
        )

        # Создаём движок SQLAlchemy
        engine = create_engine(conn_string)

        # Проверяем подключение
        with engine.connect() as conn:
            print(f"Успешно подключились к {db_settings['url']}:{db_settings['port']} → {db_name}")

        # Берём только первые 100 строк
        df_limited = df.head(100).copy()

        # Загружаем в PostgreSQL
        df_limited.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",
            index=False,
            method="multi"
        )

        print(f"Данные успешно записаны в public.{table_name}")
        return engine

    except Exception as e:
        print(f"Ошибка при загрузке в базу {db_name}: {e}")
        return None


# Проверка результата в базе

def show_table_data(engine, table_name, rows_to_show=5):
  
    # Выводит первые строки и структуру таблицы в базе данных
    try:
        # Получаем несколько строк из таблицы
        preview = pd.read_sql(
            f'SELECT * FROM public."{table_name}" LIMIT {rows_to_show}',
            engine
        )
        print(f"\nПервые {rows_to_show} строк из public.{table_name}:")
        print(preview)

        # Проверяем структуру таблицы
        table_info = pd.read_sql(
            """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema='public' AND table_name=%(tname)s 
            ORDER BY ordinal_position
            """,
            engine,
            params={"tname": table_name}
        )
        print(f"\nСтруктура таблицы public.{table_name}:")
        print(table_info)
        return True

    except Exception as e:
        print(f"Ошибка при чтении таблицы: {e}")
        return False



# Основная функция

def main():
    print("=" * 50)
    print("ПРОГРАММА ДЛЯ ЗАГРУЗКИ ДАННЫХ В PostgreSQL (public.khabibullina)")
    print("=" * 50)

    # Получаем параметры подключения
    db_settings = get_connection_settings()
    if db_settings is None:
        print("Не удалось получить настройки подключения!")
        return

    # Загружаем данные
    df = load_data()
    if df is None:
        print("Не удалось загрузить данные!")
        return

    print(f"\nЗагружено {len(df)} строк")
    print(f"Колонки: {list(df.columns)}")

    # Загружаем данные в базу
    print("\n" + "=" * 50)
    print("ЗАГРУЗКА ДАННЫХ В БАЗУ HOMEWORKS → public.khabibullina")
    print("=" * 50)

    engine = upload_to_database(df, db_settings, "homeworks", "khabibullina")

    # Проверка результата
    if engine is not None:
        ok = show_table_data(engine, "khabibullina")

        try:
            row_count = pd.read_sql(
                f'SELECT COUNT(*) FROM public."khabibullina"',
                engine
            ).iloc[0, 0]
            print(f"\nКоличество строк в таблице: {row_count}")
        except Exception as e:
            print(f"Ошибка при подсчёте строк: {e}")

        if ok:
            print("\n" + "=" * 50)
            print("ЗАГРУЗКА УСПЕШНО ЗАВЕРШЕНА.")
            print("=" * 50)
        else:
            print("Данные записаны, но проверка прошла с ошибками.")
    else:
        print("Ошибка при подключении к базе или загрузке данных.")


# Точка входа

if __name__ == "__main__":
    main()