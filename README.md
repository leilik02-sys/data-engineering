#  Dataset: Historical CO₂ data with energy, economy, and population indicators (1850-2023)

> [!NOTE]
><strong>About this file</strong>
><p>This file provides a historical view of global CO₂ and greenhouse gas (GHG) emissions across countries, regions, economic groups, and sectors. It includes detailed information on population, GDP, energy use, and emissions from cement, coal, oil, gas, flaring, and land-use change.</p> <p>The data is sourced from Our World in Data, a trusted platform for global statistics. Each row represents a country (or group/sector) in a given year, with values for per capita emissions, emissions per GDP, cumulative emissions, and contributions to global climate change.</p><p>In addition to CO₂, the dataset contains methane, nitrous oxide, and total GHG emissions, along with energy consumption and trade-related CO₂ indicators. It also reports global shares and estimates of temperature change caused by different greenhouse gases. It consists of 50 columns in total.</p>
<ol>
Links:
<p><li>link to the dataset:
https://drive.google.com/file/d/14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X/view?usp=sharing</li>
<p><li>original source of the dataset:
https://www.kaggle.com/datasets/shreyanshdangi/co-emissions-across-countries-regions-and-sectors/data</li>
</ol> 
__________________________________________

<strong>Description</strong>

>This project demonstrates how to set up a Python environment with Conda and Poetry, load a dataset from Google Drive, and preview the first 10 rows using pandas.
The main script is `data_loader.py`, which downloads the dataset and prints a quick preview for validation.

---
#### Project Structure

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
│   │   ├── api_reader.py
│   │   ├── environment.yml
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── requirements.txt
│   
│   ├── parse_example/        # Data parsing examples
│   ├── data_parser.py
│   ├── environment.yml
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt
├── notebook/                 # Jupyter notebooks
│   └── EDA.ipynb             # Exploratory Data Analysis

├── .gitignore
├── environment.yml           # Conda environment configuration
├── pyproject.toml           # Python project configuration
├── README.md
└── requirements.txt         # Python dependencies
```

---
> [!IMPORTANT]
> #### Prerequisites
>
>Before getting started, make sure you have the following installed: 
>
> - Python 3.7+
> - Conda (miniconda/anaconda)
> - pip (Python package manager)
> - Installed packages: pandas, numpy, pyarrow, black


## Virtual Environment Setup

<ol>

<li>Create a virtual environment
<p>conda create -n my_env python=3.13</p>
<p>pip conda activate my_env</p>
<li>Install poetry
<p>pip install poetry</p>
<li>Initialize project
<p>poetry new my_project</p>
<li>Add dependencies
<p>poetry add jupyterlab pandas matplotlib wget</p>
</p>
<li>Install
</ol>
<p>poetry install -no-root</p>

#### Run the Script
<p>python3 data_loader.py</p>


```

<strong>Dependencies</strong>

The project uses several Python libraries for data analysis and prototyping:
- pandas — for loading and processing tabular data
- matplotlib — for basic data visualization
- wget — for downloading files (if needed)
- jupyterlab — for interactive notebooks and prototyping

#### Script Output
<img width="1228" height="276" alt="Снимок экрана 2025-09-20 в 10 19 54" src="https://github.com/user-attachments/assets/39b6dbb3-dc34-4dbf-af89-ea1c0c95b388" />

### Analyze data types
<ol>

<li>First, you need to see how the raw dataset looks before any changes.
<p>  Look at the first rows (head (10))— to understand the structure.</p>
<li> Run info() to see column types (int, float, object, etc.) and how many values are non-null vs. missing.
<li>Count missing values (isnull().sum()) to identify potential problems.
<li>For text columns (object):
<p> - Сheck how many unique values exist </p>
<p> - For numeric columns, use describe() — check min, max, mean, etc. to spot outliers or strange numbers.</p>
</ol>

#### Example:
<img width="548" height="700" alt="Снимок экрана 2025-09-30 в 17 31 55" src="https://github.com/user-attachments/assets/4685aba7-a0bb-44a6-9390-b658c3583491" />
<img width="593" height="689" alt="Снимок экрана 2025-09-30 в 17 32 27" src="https://github.com/user-attachments/assets/e515636e-17d7-4bd4-a831-1bca4a4ad61d" />
<img width="877" height="406" alt="Снимок экрана 2025-09-30 в 17 33 04" src="https://github.com/user-attachments/assets/546d4e54-2eb9-42c6-9fed-bbd1d632c5c0" />

###  Cast data types
<ol>
<li>Once you understand the current state, you fix column types to make analysis easier:
<p>year to datetime64[ns].
<p>*This makes filtering, slicing, and time-series analysis straightforward.*
<p>population to Int64 (nullable integer).
<p>*Population is always an integer, but some rows may have missing values (NaN). Using nullable Int64 keeps it integer while still allowing NaN.*
<li>Repeated category-like columns (iso_code, Name, Description) to category.
<p>*This reduces memory usage and speeds up operations like grouping.*
<li>After casting, print dtypes, info(), and missing value counts again to verify everything worked.
<li>Compare memory usage before and after — you’ll usually see significant savings, especially for text columns.
</ol>

### Save results
<p>To keep your work:
<p>Save the cleaned dataset as Parquet (Data_clean.parquet), it’s compact, fast, and preserves data types.
<p>Optionally also save to CSV if you want to open it in Excel or Google Sheets.
 
### Example
<img width="621" height="689" alt="Снимок экрана 2025-09-30 в 17 44 13" src="https://github.com/user-attachments/assets/7aca9a48-3f20-4927-ab71-2dbe281aabc3" />
<img width="672" height="706" alt="Снимок экрана 2025-09-30 в 17 44 51" src="https://github.com/user-attachments/assets/7a3a1dcd-cced-46fd-aab9-a27d68657e79" />
<img width="710" height="717" alt="Снимок экрана 2025-09-30 в 17 45 02" src="https://github.com/user-attachments/assets/f779bcee-398d-495f-9fdc-0acf11ed5f54" />

__________________________________________

## Running the ETL Pipeline

The ETL process can be executed directly from the command line.

**1.Run the full pipeline**
```bash
python etl/main.py --file_id <GoogleDrive_file_ID> --table <table_name>
```
*Example:*

```bash
python etl/main.py --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X --table khabibullina
```
**2.Command Line Arguments**

| **Parameter** | **Description**                         | **Example**                                     |
|---------------|------------------------------------------|-------------------------------------------------|
| `--file_id`   | Google Drive file ID of the dataset      | `--file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X`   |
| `--table`     | Name of the PostgreSQL table to write to | `--table khabibullina`                          |
**3.ETL Functionality**

| **Stage**     | **Module**       | **Description**                                                                       |
|----------------|------------------|----------------------------------------------------------------------------------------|
| **Extract**   | `etl.extract`    | Downloads the CSV dataset from Google Drive → `data/raw/raw_data.csv`                 |
| **Transform** | `etl.transform`  | Converts data types, cleans columns, validates → `data/processed/clean_data.parquet`  |
| **Load**      | `etl.load`       | Loads ≤100 rows into PostgreSQL and adds primary key `id`                             |
| **Main**      | `etl.main`       | Connects all stages and provides a CLI interface                                      |

**4.Example Output**

```bash
(my_env) MacBook-Air-Lejla:my_project lejla$ python etl/main.py --file_id 14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X --table khabibullina

[RUN] Start ETL
[EXTRACT] Сырые данные сохранены в data/raw/raw_data.csv
[TRANSFORM] Данные обработаны и сохранены в data/processed/clean_data.parquet
[LOAD] Загружено 100 строк в таблицу khabibullina
[DONE] ETL завершен
```
**5.Validation**

If you implement `validate.py`, it can:

- Check data integrity and duplicates  
-  Verify type consistency  
-  Compare record counts between **Parquet** and **PostgreSQL**
---

##  .gitignore Example
.env
__pycache__/
.ipynb_checkpoints/
*.csv
*.parquet
data/raw/
data/processed/



