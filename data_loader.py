import pandas as pd

FILE_ID = "14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

raw_data = pd.read_csv(file_url)  # читаем файл
print(raw_data.head(10))  # выводим на экран первые 10 строк для проверки

import pandas as pd

FILE_ID = "14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

df = pd.read_csv(file_url)  # загрузка файла

print("\n Первые строки исходных данных:")
print(df.head(10))

print("\n Общая информация о датасете:")
print(df.info())  # просмотр всех типов столбцов и значений, в том числе сколько NaN

print("\n Кол-во пропусков по столбцам:")
print(df.isnull().sum())  # посчитать пустые значения для всех столбцов

print("\n Уникальные значения для текстовых колонок:")
for col in df.select_dtypes(include=["object"]).columns:
    print(col, df[col].nunique(), df[col].unique()[:10])  # просмотр уникальных значений

print("\n Статистика для числовых колонок:")
print(df.describe())  # для числовых колонок просмотр минимума, максимума и среднего

print("\n Типы ДО приведения:")
print(df[["year", "population", "iso_code", "Name", "Description"]].dtypes)

df["year"] = pd.to_datetime(
    df["year"].astype(str), format="%Y", errors="coerce"
)  # приведение типов year to datetime
df["population"] = pd.to_numeric(df["population"], errors="coerce").astype(
    "Int64"
)  # приведение типов population to Int64

if "iso_code" in df.columns:  # признаки по категориям
    df["iso_code"] = df["iso_code"].astype("category")
if "Name" in df.columns:  # признаки по категориям
    df["Name"] = df["Name"].astype("category")
if "Description" in df.columns:  # признаки по категориям
    df["Description"] = df["Description"].astype("category")

print("\n Типы ПОСЛЕ приведения:")
print(df[["year", "population", "iso_code", "Name", "Description"]].dtypes)

print("\n Общая информация ПОСЛЕ приведения:")
print(df.info())

print("\n Пропуски ПОСЛЕ приведения:")
print(df.isnull().sum())

out_path = "Data_clean.parquet"
df.to_parquet(out_path, index=False)
print(f"\n[OK] Данные загружены, приведены к нужным типам и сохранены в {out_path}")
