# РБК news Parser

This folder contains a simple **web scraping script** that collects news headlines and links  
from the [RBC Economics section](https://www.rbc.ru/economics/).

## Description

The script `data_parser.py`:
- sends an HTTP request to the RBC website;
- parses the HTML page using **BeautifulSoup**;
- extracts article titles and URLs;
- saves the collected data as a `.json` file with the current date in its name (e.g. `rbc_articles_07_10_2025.json`).

Each run of the script creates a new JSON file in the same directory (`parse_example`).

## Technologies Used

- `requests` — for making HTTP requests  
- `beautifulsoup4` — for parsing HTML content  
- `fake-useragent` — to randomize browser headers and avoid blocking  
- `lxml` — as the HTML parser  

##  Installation

To install dependencies, activate your virtual environment and run:

```bash
pip install beautifulsoup4 requests fake-useragent lxml
```
## How to Run

```bash
python my_project/parse_example/data_parser.py
```
If the script executes successfully, you’ll see output like this:

#### Example
<img width="878" height="72" alt="Снимок экрана 2025-10-07 в 19 56 49" src="https://github.com/user-attachments/assets/fc84e8ad-78d8-4d33-ba5e-406ea1a52194" />

#### Example of Saved JSON File
<img width="1123" height="465" alt="Снимок экрана 2025-10-07 в 19 59 37" src="https://github.com/user-attachments/assets/56c34ded-6e89-450c-bc5e-e225f275671e" />


  ### Project Structure
my_project/
├── api_example/
│   ├── api_reader.py
│   ├── README.md 
│   ├── screenshot.png
│   ├── action_16.json 
│   ├── action_27.json 
│   └──  action_127.json
├── parse_example/
│   ├── data_parser.py
│   ├── README.md
│   └── rbc_articles_07_10_2025.json
└── README.md
