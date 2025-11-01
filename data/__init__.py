"""
ETL package.

extract.py   — загрузка сырых данных (.csv → data/raw)
transform.py — приведение типов и сохранение .parquet → data/processed
load.py      — запись в PostgreSQL (max 100 строк)
main.py      — CLI-интерфейс запуска ETL

Использование из консоли:
    python etl/main.py --file_id <GoogleDriveID> --table khabibullina
"""

from .extract import extract
from .transform import transform
from .load import load_to_db

__all__ = ["extract", "transform", "load_to_db"]
