import argparse
from .extract import extract
from .transform import transform
from .load import load_to_db
from dotenv import load_dotenv
load_dotenv()


def cli():
    parser = argparse.ArgumentParser(description="ETL pipeline")
    parser.add_argument("--file_id", required=True, help="ID файла на Google Drive")
    parser.add_argument("--table", default="khabibullina", help="Имя таблицы в БД")
    args = parser.parse_args()

    print("[RUN] Start ETL")

    raw = extract(args.file_id)
    processed = transform(raw)
    load_to_db(processed, args.table)

    print("[DONE] ETL завершен")


if __name__ == "__main__":
    cli()
