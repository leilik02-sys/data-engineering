import pandas as pd
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

def get_connection_settings():
   
    """
    Возвращаем параметры подключения к PostgreSQL из переменных окружения.
    """
    try:
        settings = {
            "url": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT", "5432"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME", "homeworks"),
        }

        # Проверка, что обязательные значения заданы
        missing = [k for k, v in settings.items() if not v]
        if missing:
            print("Ошибка: отсутствуют переменные окружения:", ", ".join(missing))
            return None

        return settings
    except Exception as e:
        print(f"Ошибка при получении настроек подключения: {e}")
        return None

# Загрузка данных
def load_data():
    
    # Загружаем данные из локального Data_clean.parquet, если нет, то скачиваем CSV из Google Drive и делаем приведение типов
    
    try:
        # Проверяем, есть ли готовый parquet 
        if os.path.exists("Data_clean.parquet"):
            print("Файл Data_clean.parquet найден — загружаем его.")
            df = pd.read_parquet("Data_clean.parquet")
            print(f"Загружено {len(df)} строк.")
            return df

        # Если parquet нет, качаем с Google Drive 
        print("Файл не найден. Загружаем исходные данные из Google Drive...")
        FILE_ID = "14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X"
        file_url = f"https://drive.google.com/uc?id={FILE_ID}"

        df = pd.read_csv(file_url)
        print(f"Загружено {len(df)} строк из Google Drive.")

        # Приведение типов 
        if "year" in df.columns:
            df["year"] = pd.to_datetime(df["year"].astype(str), format="%Y", errors="coerce")
        if "population" in df.columns:
            df["population"] = pd.to_numeric(df["population"], errors="coerce").astype("Int64")
        for col in ["iso_code", "Name", "Description"]:
            if col in df.columns:
                df[col] = df[col].astype("category")

        # Сохраняем чистые данные локально
        df.to_parquet("Data_clean.parquet", index=False)
        print("Файл Data_clean.parquet создан для последующего использования.")
        return df

    except Exception as e:
        print(f"Ошибка при загрузке или обработке данных: {e}")
        return None

# Запись в PostgreSQL

def upload_to_database(df: pd.DataFrame, db_settings: dict, table_name: str):
    """
    Записываем максимум 100 строк DataFrame в таблицу public.<table_name>.
    Подключение формируем через URL.create.
    """
    try:
        # Безопасная сборка URL 
        url = URL.create(
            drivername="postgresql+psycopg2",
            username=db_settings["user"],
            password=db_settings["password"],
            host=db_settings["url"],
            port=int(db_settings["port"]),
            database=db_settings["dbname"],
        )

        engine = create_engine(url)
        print(f"Подключение к базе {db_settings['dbname']}...")

        # Проверка соединения простым запросом
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Соединение успешно установлено.")

        # Записываем не более 100 строк
        df_limited = df.head(100).copy()

        # Запись в схему public
        df_limited.to_sql(
            name=table_name,
            con=engine,
            schema="public",
            if_exists="replace",   # при повторном запуске пересоздаём
            index=False,
            method="multi"
        )

        print(f"Данные успешно загружены в public.{table_name}")
        return engine

    except Exception as e:
        print(f"Ошибка при загрузке в базу данных: {e}")
        return None


# Самопроверка, просмотр первых строк и структуры таблицы

def show_table_data(engine, table_name: str, rows_to_show: int = 5):
    try:
        preview = pd.read_sql(
            f'SELECT * FROM public."{table_name}" LIMIT {rows_to_show}',
            engine
        )
        print(f"\nПервые {rows_to_show} строк из public.{table_name}:")
        print(preview)

        table_info = pd.read_sql(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema='public' AND table_name=%(tname)s
            ORDER BY ordinal_position
            """,
            engine,
            params={"tname": table_name},
        )
        print(f"\nСтруктура public.{table_name}:")
        print(table_info)
        return True
    except Exception as e:
        print(f"Ошибка при чтении таблицы: {e}")
        return False

# Точка входа

def main():
    print("=" * 50)
    print("Программа загрузки данных В PostgreSQL (public.khabibullina)")
    print("=" * 50)

    db_settings = get_connection_settings()
    if not db_settings:
        print("Не удалось получить параметры подключения.")
        return

    df = load_data()
    if df is None:
        print("Не удалось загрузить данные.")
        return

    print(f"\nВсего строк в датасете: {len(df)}")
    print(f"Колонки: {list(df.columns)}")

    print("\n" + "=" * 50)
    print("ЗАГРУЗКА ДАННЫХ В БАЗУ homeworks в public.khabibullina")
    print("=" * 50)

    engine = upload_to_database(df, db_settings, table_name="khabibullina")

    if engine is not None:
        ok = show_table_data(engine, "khabibullina")
        # ...
    else:
        print("Ошибка: данные не были загружены в базу.")


if __name__ == "__main__":
    main()