def validate_dataframe(df):
    if df.empty:
        raise ValueError("Датасет пуст!")

    if "population" in df.columns and df["population"].isna().all():
        raise ValueError("Колонка population состоит только из NaN")
