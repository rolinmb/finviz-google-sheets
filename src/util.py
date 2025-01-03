import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

CREDENTIALFILE = "src/first-footing-446718-m6-c9b09bd18afc.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(CREDENTIALFILE, scopes=SCOPES)
SPREADSHEETID = "finviz-google-sheets"
service = build("sheets", "v4", credentials=CREDS)
sheet = service.spreadsheets()

FVURL = "https://finviz.com/quote.ashx?t="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def check_user_input(ticker):
    if len(ticker) > 4:
        raise ValueError('src/util.py : check_user_input() :: ERROR ::: Underlying name must be at most 4 alphabetical characters.')
    if not ticker.isalpha():
        raise ValueError('src/util.py : check_user_input() :: ERROR ::: Underlying name must only contain alphabetical characters.')
    return ticker.upper()


def fetch_finviz(ticker):
    response = requests.get(FVURL+ticker, headers=HEADERS)
    response.raise_for_status()
    print("src/util.py : fetch_finviz() :: Successfully fetched finviz.com html for $"+ticker)
    soup = BeautifulSoup(response.text,  "html.parser")
    table = soup.find("table", class_="js-snapshot-table snapshot-table2 screener_snapshot-table-body")
    data = []
    for row in table.find_all("tr", class_="table-dark-row"):
        row_data = []
        for cell in row.find_all("td"):
            cell_text = cell.get_text(strip=True)
            row_data.append(cell_text)
        data.append(row_data)
    data_dict = {}
    for row in data:
        for i in range(0, len(row), 2):
            label = row[i]
            value = row[i + 1] if i+1 < len(row) else None
            data_dict[label] = value
    print("src/util.py : fetch_finviz() :: Successfully parsed finviz.com html table for $"+ticker)
    return data_dict

def upload_data_dict(data_dict):
    headers = list(data_dict.keys())
    values = list(data_dict.values())
    new_data = [headers, values]
    RANGE = "Sheet1!A1"
    sheet.values().update(
        spreadsheetId = SPREADSHEETID,
        range=RANGE,
        valueInputOption="RAW",
        body={ "values": new_data }
    ).execute()
    print("src/util.py : upload_data_dict() :: Successfully uploaded finviz.com html table data to google drive sheet")