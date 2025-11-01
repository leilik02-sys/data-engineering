import pandas as pd
import os


def transform(raw_path: str) -> str:
    """Обрабатывает raw CSV → приводит типы → сохраняет parquet"""

    df = pd.read_csv(raw_path)

    df["year"] = pd.to_datetime(df["year"].astype(str), format="%Y", errors="coerce")
    df["population"] = pd.to_numeric(df["population"], errors="coerce").astype("Int64")

    for col in ["iso_code", "Name", "Description"]:
        if col in df.columns:
            df[col] = df[col].astype("category")

    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/clean_data.parquet"

    df.to_parquet(out_path, index=False)
    print(f"[TRANSFORM] Данные обработаны и сохранены в {out_path}")

    return out_path
