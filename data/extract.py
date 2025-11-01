import pandas as pd
import os


def extract(file_id: str) -> str:
    """Скачивает CSV с Google Drive и сохраняет в data/raw"""

    url = f"https://drive.google.com/uc?id={file_id}"
    raw_path = "data/raw/raw_data.csv"

    try:
        df = pd.read_csv(url)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки CSV: {e}")

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(raw_path, index=False)

    print(f"[EXTRACT] Сырые данные сохранены в {raw_path}")
    return raw_path
