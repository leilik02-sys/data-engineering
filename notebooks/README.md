# CO₂ Emissions Data Engineering Project

This repository contains an ETL pipeline for the **processing and analysis of historical CO₂ emissions data**.  
The project demonstrates a complete workflow — from data extraction to database integration and exploratory data analysis (EDA).  
Developed as part of the **Data Engineering** course at **ITMO University (2025)**.  
Written in **Python 3.13**.

---

## Project Overview

The main objectives of this project:
- Extraction of historical CO₂ data from Google Drive  
- Preprocessing, cleaning, and type transformation  
- Storage of processed data in Parquet and PostgreSQL  
- Exploratory Data Analysis (EDA) for identifying global emission trends  

The project illustrates fundamental **data engineering** concepts and best practices for building reproducible ETL pipelines.

---

## Dataset

The dataset used in this project is available here:  
[📎 CO₂ dataset (Google Drive)](https://drive.google.com/file/d/14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X/view?usp=sharing)

**Source:** [Kaggle – CO₂ Emissions Across Countries, Regions, and Sectors](https://www.kaggle.com/datasets/shreyanshdangi/co-emissions-across-countries-regions-and-sectors/data)  
**Period covered:** 1850–2023  
**Contents:** Indicators on CO₂, CH₄, N₂O emissions, energy use, GDP, and population across countries and sectors.

The dataset is automatically downloaded and processed by the ETL pipeline.

---

## Project Structure

```
MY-PROJECT/
├── etl/                      # ETL pipeline package
│   ├── __init__.py
│   ├── extract.py           # Data loading from Google Drive
│   ├── transform.py         # Data transformation and cleaning
│   ├── load.py              # Loading to DB and export to parquet
│   ├── validate.py          # Data validation
│   └── main.py              # CLI entry point
│── src
│   │
├── api_example/              # API examples and integration
│   ├── api_reader.py
│   ├── environment.yml
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt
├── notebook/                 # Jupyter notebooks
│   └── EDA.ipynb            # Exploratory Data Analysis
├── parse_example/            # Data parsing examples
│   ├── data_parser.py
│   ├── environment.yml
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt
├── .gitignore
├── pyproject.toml           # Python project configuration
├── README.md
└── requirements.txt         # Python dependencies
```

---

## Installation and Setup

Follow these steps to set up the environment and run the project:

### 1. Create and activate a Conda environment
```bash
conda create -n my_env python=3.13 -y
conda activate my_env
```
### 2. Install dependencies 
```bash
pip install pandas pyarrow sqlalchemy psycopg2-binary python-dotenv
```
### 3. Configure database credentials

Create a `.env` file in the root of the project

### 4. ETL Pipeline Usage

The ETL process can be executed directly via command line.
 
 **Run the Full Pipeline**
You can execute the complete ETL process using the command below:

```bash
python etl/main.py --file_id <GoogleDrive_file_ID> --table <table_name>
```
```bash
--file_id — Google Drive file ID of the dataset
--table — PostgreSQL table name for storing the processed data
```

**Running Individual Stages**

You can also execute each stage of the ETL process separately:

# Extract stage – download raw data from Google Drive
python -m etl.main extract --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X

# Transform stage – clean and typecast raw data
python -m etl.main transform --input data/raw/raw_data.csv

# Load stage – upload cleaned data into PostgreSQL
python -m etl.main load --input data/processed/clean_data.parquet --table khabibullina

### 5. **ETL Functionality**

#### **Extract**
-  Downloads the CSV dataset directly from **Google Drive**  
- Saves it locally in  
  `data/raw/raw_data.csv`

#### **Transform**
-  Converts the **year** column to `datetime` format  
-  Casts **population** to a nullable integer (`Int64`)  
-  Converts text columns — `iso_code`, `Name`, `Description` — to **categorical** types  
-  Saves the cleaned and transformed data as Parquet →  
  `data/processed/clean_data.parquet`

#### **Load**
-  Uploads up to **100 rows** into the PostgreSQL table (adds primary key `id`)  
-  Validates schema and data structure before insertion  
-  Prints confirmation message upon successful completion

**Example Run Output**
```bash
(my_env) MacBook-Air-Lejla:my_project lejla$ python -m etl.main --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X --table khabibullina
```
[RUN] Start ETL
[EXTRACT] Сырые данные сохранены в data/raw/raw_data.csv
[TRANSFORM] Данные обработаны и сохранены в data/processed/clean_data.parquet
[LOAD] Загружено 100 строк в таблицу khabibullina
[DONE] ETL завершен


