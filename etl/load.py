import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()


def load_to_db(parquet_path: str, table_name: str):
    """Записывает данные (max 100 строк) в PostgreSQL"""

    df = pd.read_parquet(parquet_path).head(100)

    df = df.reset_index(drop=True)
    df["id"] = df.index + 1
    df = df.loc[:, ["id"] + [c for c in df.columns if c != "id"]]

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    engine = create_engine(url)

    df.to_sql(table_name, engine, if_exists="replace", index=False, method="multi")

    with engine.begin() as con:
        con.execute(text(f'ALTER TABLE "{table_name}" ADD PRIMARY KEY (id)'))

    print(f"[LOAD] Загружено {len(df)} строк в таблицу {table_name}")
