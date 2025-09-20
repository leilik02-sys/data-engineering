#  Dataset: Historical CO₂ data with energy, economy, and population indicators (1850-2025)

<strong>About this file</strong>

><p>This file provides a historical view of global CO₂ and greenhouse gas (GHG) emissions across countries, regions, economic groups, and sectors. It includes detailed information on population, GDP, energy use, and emissions from cement, coal, oil, gas, flaring, and land-use change.</p> <p>The data is sourced from Our World in Data, a trusted platform for global statistics. Each row represents a country (or group/sector) in a given year, with values for per capita emissions, emissions per GDP, cumulative emissions, and contributions to global climate change.</p><p>In addition to CO₂, the dataset contains methane, nitrous oxide, and total GHG emissions, along with energy consumption and trade-related CO₂ indicators. It also reports global shares and estimates of temperature change caused by different greenhouse gases. It consists of 50 columns in total.</p>

<ol>**Links:**
<p><li>link to the dataset:
https://drive.google.com/file/d/14wKDsdZ1HnI1-zcAPB59HnHJq6Th2z3X/view?usp=sharing</li>
<p><li>original source of the dataset:
https://www.kaggle.com/datasets/shreyanshdangi/co-emissions-across-countries-regions-and-sectors/data</li>
</ol> 
__________________________________________

<strong>Description</strong>

>This project demonstrates how to set up a Python environment with Conda and Poetry, load a dataset from Google Drive, and preview the first 10 rows using pandas.
The main script is `data_loader.py`, which downloads the dataset and prints a quick preview for validation.


>#### Prerequisites
>>
>>Before getting started, make sure you have the following installed: 
>>
>> - Python 3.7+
>> - Conda (miniconda/anaconda)
>> - pip (Python package manager)

#### Virtual Environment Setup

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

**Run the Script**
<p>python3 data_loader.py</p>

**Project Structure**

<pre>
 data-engineering/ 

├── data_loader.py     
 # Script for downloading and previewing dataset

├── pyproject.toml       
# Poetry configuration file (dependencies and metadata)

├── poetry.lock         
 # Locked dependency versions

├── requirements.txt     
# Alternative dependencies file (for pip users)

└── README.md           
 # Project documentation </pre>

<strong>Dependencies</strong>

The project uses several Python libraries for data analysis and prototyping:
- pandas — for loading and processing tabular data
- matplotlib — for basic data visualization
- wget — for downloading files (if needed)
- jupyterlab — for interactive notebooks and prototyping

# Script Output
<img width="1228" height="276" alt="Снимок экрана 2025-09-20 в 10 19 54" src="https://github.com/user-attachments/assets/39b6dbb3-dc34-4dbf-af89-ea1c0c95b388" />
