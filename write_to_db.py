import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

def env():
    vals = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME"),
        "table": os.getenv("TABLE_NAME")
    }
    missing = [k for k, v in vals.items() if not v]
    if missing:
        print("Отсутствуют переменные окружения:", ", ".join(missing))
        sys.exit(1)
    return vals

def load_parquet(path="Data_clean.parquet"):
    if not os.path.exists(path):
        print("Файл данных не найден")
        sys.exit(1)
    try:
        df = pd.read_parquet(path)
    except (ValueError, OSError):
        print("Ошибка чтения parquet")
        sys.exit(1)
    if df.empty:
        print("Датасет пуст")
        sys.exit(1)
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    df = df.reset_index(drop=True)
    df["id"] = df.index + 1
    cols = ["id"] + [c for c in df.columns if c != "id"]
    return df.loc[:, cols].head(100)

def engine_from_env(cfg):
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=cfg["user"],
        password=cfg["password"],
        host=cfg["host"],
        port=int(cfg["port"]),
        database=cfg["dbname"],
    )
    try:
        eng = create_engine(url, pool_pre_ping=True)
        with eng.connect() as c:
            c.execute(text("SELECT 1"))
        return eng
    except OperationalError as e:
        with open("errors.log", "a") as f:
            f.write(f"DB connect error: {e}\n")
        print("Не удаётся подключиться к БД (подробности в errors.log)")
        sys.exit(1)

def write_table(df, eng, table):
    try:
        df.to_sql(table, eng, schema="public", if_exists="replace", index=False, method="multi")
        with eng.begin() as c:
            c.execute(text(f'ALTER TABLE public."{table}" DROP CONSTRAINT IF EXISTS {table}_pkey'))
            c.execute(text(f'ALTER TABLE public."{table}" ADD PRIMARY KEY (id)'))
    except ProgrammingError as e:
        with open("errors.log", "a") as f:
            f.write(f"SQL error write_table: {e}\n")
        print("Ошибка записи в таблицу (подробности в errors.log)")
        sys.exit(1)
    except SQLAlchemyError as e:
        with open("errors.log", "a") as f:
            f.write(f"SQLAlchemy error write_table: {e}\n")
        print("Ошибка при работе с базой (подробности в errors.log)")
        sys.exit(1)

def preview(eng, table):
    try:
        head = pd.read_sql(f'SELECT * FROM public."{table}" ORDER BY id LIMIT 5', eng)
        info = pd.read_sql(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_schema='public' AND table_name=%(t)s ORDER BY ordinal_position",
            eng,
            params={"t": table},
        )
        check_pk = pd.read_sql(
            "SELECT constraint_name FROM information_schema.table_constraints "
            "WHERE table_schema='public' AND table_name=%(t)s AND constraint_type='PRIMARY KEY'",
            eng,
            params={"t": table},
        )
        print("\nПервые 5 строк:")
        print(head)
        print("\nСтруктура:")
        print(info)
        print("\nПервичный ключ:")
        print(check_pk if not check_pk.empty else "нет")
    except SQLAlchemyError as e:
        with open("errors.log", "a") as f:
            f.write(f"SQL error preview: {e}\n")
        print("Ошибка при чтении таблицы (подробности в errors.log)")
        sys.exit(1)

def main():
    cfg = env()
    print("Запуск загрузки данных в базу")
    df = load_parquet("Data_clean.parquet")
    print(f"Строк в датасете: {len(df)}")
    eng = engine_from_env(cfg)
    write_table(df, eng, cfg["table"])
    preview(eng, cfg["table"])

if __name__ == "__main__":
    main()
