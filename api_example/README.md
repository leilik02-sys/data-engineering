# Working with the XIVAPI

This example demonstrates how to fetch data about character actions  
from the public **Final Fantasy XIV API** — [https://xivapi.com/Action](https://xivapi.com/Action)


## Description

The script [`api_reader.py`](./api_reader.py) requests data from the XIVAPI,  
retrieves a JSON response, and converts it into a **Pandas DataFrame**.  
It also cleans up HTML tags and flattens nested structures for easier analysis.

All raw JSON files are saved into the `xiv_data` folder for reference.


## Technologies Used
- Python 3.10+
- `requests` — for sending HTTP requests  
- `pandas` — for tabular data processing  
- `json` — for working with structured data


## How to Run

```bash
python api_reader.py
```
#### After running, the script will:
-  Fetch multiple **Actions** by their IDs  
-  Display their **names in English and Japanese**  
-  Show key parameters such as `Cast100ms`, `Range`, and `CooldownGroup`  
-  Output a formatted **DataFrame** in the console

  ## Example Output
  
<img width="1145" height="230" alt="Снимок экрана 2025-10-07 в 15 28 55" src="https://github.com/user-attachments/assets/55479e53-da12-438c-b6cb-2a5177242a80" />

  
   MY_PROJECT/
├── README.md
└── api_example/
    ├── api_reader.py
    ├── screenshot.png
    └── README.md
