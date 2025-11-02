<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWtkc3M0ZDRuZXp6YmF3cG5vZGRmM2I3ajJ4ZWhlM3R4M2dnYXBoMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3o7TKsQWkP0h2fQbXK/giphy.gif" width="120" alt="ETL Globe Animation" />
</p>

<h1 align="center">🌍 ETL + EDA Data Pipeline Project</h1>  
<p align="center">
  <em>A complete Extract–Transform–Load workflow with data analysis and PostgreSQL integration.</em>
</p>

> [!NOTE]
This project presents a complete data engineering workflow for processing, transforming, validating, and analyzing historical CO₂ emission data from 1850 to 2023. The dataset combines information about population, GDP, and energy use across countries and regions.

---

## Table of Contents
1. [Dataset Overview](#dataset-overview)
2. [Project Description](#project-description)
3. [Project Structure](#project-structure)
4. [Environment Setup](#environment-setup)
5. [ETL Pipeline](#etl-pipeline)
6. [EDA (Exploratory Data Analysis)](#eda-exploratory-data-analysis)
7. [Experiments & Additional Files](#experiments--additional-files)
8. [.gitignore Example](#gitignore-example)

---

## Dataset Overview

**Dataset:** Historical CO₂, Energy, and Population Data (1850–2023)
**Source:** Our World in Data + Kaggle

Each record represents one country or region per year and includes:
- CO₂ and greenhouse gas emissions (coal, oil, gas, cement, land-use)
- Energy use, GDP, and population
- Climate and trade-related CO₂ indicators

**Links:**
- [Google Drive Dataset](https://drive.google.com/file/d/14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X/view?usp=sharing)
- [Original Kaggle Source](https://www.kaggle.com/datasets/shreyanshdangi/co-emissions-across-countries-regions-and-sectors/data)

---
##  Project Overview

> [!IMPORTANT]
> The main goal of this project is to build a **fully automated ETL pipeline** that processes historical CO₂ data,  
> stores it efficiently, and supports further analytical workflows (EDA and visualization).

**Objectives:**
- Download and validate datasets from Google Drive  
- Clean and transform large CSV data  
- Load structured data into PostgreSQL (≤100 rows)  
- Export processed data to Parquet  
- Perform exploratory analysis of CO₂ emissions, energy use, and GDP trends  

---

## Project Structure

```
data-engineering/ 
├── etl/                     # ETL pipeline package
│   ├── __init__.py
│   ├── extract.py           # Data loading from Google Drive
│   ├── transform.py         # Data transformation and cleaning
│   ├── load.py              # Loading to DB and export to parquet
│   ├── validate.py          # Data validation
│   └── main.py              # CLI entry point
├── examples
│   ├── api_example/         # API examples and integration    
│   │   └── api_reader.py
│   │   
│   │   
│   │   
│   │   
│   │
│   ├── parse_example/        # Data parsing examples
│   └── data_parser.py
│   
│   
│   
│   
│    
├── notebook/                 # Jupyter notebooks
│   └── EDA.ipynb             # Exploratory Data Analysis
│
├── .gitignore
├── environment.yml           # Conda environment configuration
├── pyproject.toml           # Python project configuration
├── README.md
└── requirements.txt         # Python dependencies
```

---

#  Dataset: Historical CO₂ data with energy, economy, and population indicators (1850-2023)

> [!NOTE]
> The dataset provides global **CO₂ and greenhouse gas emissions (1850–2023)** with indicators for population, energy, and GDP. It includes detailed information on population, GDP, energy use, and emissions from cement, coal, oil, gas, flaring, and land-use change.</p> <p>The data is sourced from Our World in Data, a trusted platform for global statistics. Each row represents a country (or group/sector) in a given year, with values for per capita emissions, emissions per GDP, cumulative emissions, and contributions to global climate change.</p><p>In addition to CO₂, the dataset contains methane, nitrous oxide, and total GHG emissions, along with energy consumption and trade-related CO₂ indicators. It also reports global shares and estimates of temperature change caused by different greenhouse gases.

**Links:**
- [ Dataset (Google Drive)](https://drive.google.com/file/d/14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X/view?usp=sharing)
- [ Original Source on Kaggle](https://www.kaggle.com/datasets/shreyanshdangi/co-emissions-across-countries-regions-and-sectors/data)

The dataset contains:
- Historical data for over 150 countries  
- ~50 columns (CO₂, CH₄, N₂O, GHGs, population, GDP, energy consumption, etc.)  
- Data from **1850 to 2023**

---

##  Installation & Setup

> [!TIP]
> Use **Conda** or **Poetry** to ensure a clean and reproducible environment for running the ETL pipeline and EDA.

---

### 1. Create and activate the virtual environment

```bash
conda create -n my_env python=3.13
conda activate my_env
```
### 2. Install dependencies

If you are using **Poetry**:
```bash
pip install poetry
poetry install --no-root
```
Or install dependencies manually with pip:
```bash
pip install pandas gdown numpy pyarrow sqlalchemy psycopg2-binary jupyterlab matplotlib seaborn plotly
```

---

## � ETL Pipeline

> [!IMPORTANT]
> The ETL (Extract – Transform – Load) pipeline automates all stages of dataset processing:
> from downloading raw data to transforming, validating, and loading it into a PostgreSQL database.

The pipeline consists of **four main scripts** located in the `etl/` directory:

| Module | File | Purpose |
|---------|------|----------|
| **Extract** | `extract.py` | Downloads the raw CSV file from Google Drive using a file ID and saves it into `data/raw/`. |
| **Transform** | `transform.py` | Cleans the dataset: converts data types, fixes missing values, and exports a processed `.parquet` file. |
| **Validate** | `validate.py` | Ensures data consistency: checks for empty datasets and validates critical columns like `population`. |
| **Load** | `load.py` | Uploads up to 100 rows of the processed data into a PostgreSQL table (default schema: `public`). |
| **Main** | `main.py` | Connects all pipeline stages and provides a CLI interface for easy execution from the terminal. |

---

###  Folder Overview

```bash
etl/
├── init.py # Initializes the ETL package
├── extract.py # Extracts raw CSV from Google Drive
├── transform.py # Cleans and converts data types
├── validate.py # Validates dataset integrity
├── load.py # Uploads data to PostgreSQL
└── main.py # Command-line entry point
```
---

###  1. Extract — Downloading the Dataset

> [!NOTE]
> This step downloads the dataset from Google Drive by file ID and saves it into `data/raw/raw_data.csv`.

**Command:** 
```bash
python -m etl.main extract --file_id <GoogleDrive_file_ID> --output dataset.csv
```

Example:
```bash
python -m etl.main extract --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X
```
**Output:**
```bash
[EXTRACT] Raw data saved to data/raw/raw_data.csv
```

### 2. Transform — Data Cleaning and Type Conversion  
[!TIP]  
Converts the year column to datetime, ensures population is integer,  
and stores the cleaned data as a .parquet file in data/processed/.

**Command:**  
```bash
python -m etl.main transform --input data/raw/raw_data.csv
```

**Output:**
```bash
[TRANSFORM] Clean data saved to data/processed/clean_data.parquet
```

### 3. Validate — Data Integrity Check
[!NOTE]
Ensures that the dataset is not empty and that key columns contain valid values.

**Command:** 
```bash
python -m etl.main validate --input data/processed/clean_data.parquet
```

**Output:**
```bash
[VALIDATE] Data integrity check passed.
```

### 4. Load — Upload to PostgreSQL
[!IMPORTANT]
Loads up to 100 rows of cleaned data into the specified PostgreSQL table.

**Command:** 
```bash
python -m etl.main load --input data/processed/clean_data.parquet --table khabibullina
```

**Output:**
```bash
[LOAD] Successfully loaded 100 rows into table 'khabibullina'
```

### 5. Run — Full Pipeline
[!TIP]
Combines all stages (extract → transform → validate → load) in one command.

**Command:** 
```bash
python etl/main.py --file_id <GoogleDrive_file_ID> --table khabibullina
```
**Example:**
```bash
python etl/main.py --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X --table khabibullina

**Output:**
```bash
[RUN] Start ETL
[EXTRACT] Raw data saved to data/raw/raw_data.csv
[TRANSFORM] Data processed and saved to data/processed/clean_data.parquet
[LOAD] 100 rows loaded into table 'khabibullina'
[DONE] ETL complete
```
---


## EDA
# **Historical CO₂, Energy, and Economic Data Analysis (EDA)**

This project presents an **Exploratory Data Analysis (EDA)** of historical data exploring the relationship between **CO₂ emissions**, **energy consumption**, and **economic development** of countries over the period **1850–2023**.

---

## **Project Contents**

- **notebooks/EDA.ipynb** — main notebook containing full analysis, visualizations, and insights.  
- **data/** — source datasets (linked via Google Drive in the notebook).  
- **results/** — *(optional)* aggregated plots and summary metrics.  

---

## **Objective**

To explore how **CO₂ emissions correlate with GDP growth and energy usage**,  
and to identify the point where developed economies show **a slowdown in emission growth despite increasing GDP**.

---

## **Country Groups**

- **Developed:** United States, Germany, Japan  
- **Emerging:** China, India, Russia  
- **Developing:** Nigeria, Indonesia, Pakistan  

---

## **Tools and Technologies**

- **Python Libraries:** Pandas, NumPy, SciPy, Pandera  
- **Visualization:** Plotly, Seaborn, Matplotlib  
- **Environment:** Jupyter Notebook (interactive analysis platform)

---

## **Key Findings**

- Dataset covers the period **1850–2023**, containing over **1,500 records**.  
- Average data completeness is around **85%**.  
- Strong correlation detected between **GDP**, **energy use**, and **CO₂ emissions**.  
- Developed countries show **decoupling of GDP growth and CO₂ emissions**,  
  while emerging and developing countries remain highly energy-dependent.

---

## **View the Notebook in nbviewer**

 [Open EDA in nbviewer](https://nbviewer.org/github/leilik02-sys/data-engineering/blob/0bf28b2/notebooks/EDA.ipynb)  
> [!IMPORTANT]

--

### Experiments & Additional Files  
[!NOTE]  
Supporting examples and scripts located in the `experiments/` directory.  

| Path | Description |
| ---- | ------------ |
| `experiments/api_example` | API ingestion examples |
| `experiments/parse_example` | Parsing demonstrations |
| `experiments/legacy/write_to_db.py` | Legacy DB upload example |
| `experiments/legacy/read_from_db.py` | PostgreSQL reading example |

--

### .gitignore Example  
[!TIP]  
Add the following to `.gitignore` to avoid committing large or temporary files.  

```bash
# Environment and cache
.env
__pycache__/
.ipynb_checkpoints/
*.pyc
*.pyo

# Data and outputs
data/
*.csv
*.parquet

--

### Summary  
[!NOTE]  
The project delivers a full ETL + EDA workflow and meets the technical and structural requirements of the Data Engineering course (Lecture 8).  

- Automated data ingestion and cleaning  
- PostgreSQL database integration  
- Modular design for maintainability  
- Analytical insights from CO₂ historical data  
- Clean documentation and reproducible setup









