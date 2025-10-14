# РБК news Parser

This folder contains a simple **web scraping script** that collects news from the [RBC Economics section](https://www.rbc.ru/economics/).

## Description

The script `data_parser.py`:
1. Sends an HTTP request to the RBC website.  
2. Parses the HTML page using **BeautifulSoup**.  
3. Extracts article titles and URLs.  
4. Saves the collected data as a `.json` file with the current date in its name (for example:  
   `rbc_articles_14_10_2025.json`). 

Each run of the script creates a new JSON file in the same directory (`parse_example`).

## Technologies Used

1. **requests** — for sending HTTP requests
2. **beautifulsoup4** — for parsing HTML content
3. **lxml** — used as the HTML parser  

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
<img width="845" height="131" alt="Снимок экрана 2025-10-14 в 13 14 20" src="https://github.com/user-attachments/assets/c6660d40-4ebe-4b83-9c61-d722f3d3bb44" />

#### Example of Saved JSON File
<img width="1114" height="427" alt="Снимок экрана 2025-10-14 в 13 15 48" src="https://github.com/user-attachments/assets/21ab04c6-b411-4b6d-86d7-510afa2a79e0" />


  ### Project Structure
```
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
│   ├── screenshot.png
│   └── rbc_articles_14_10_2025.json
└── README.md
```
