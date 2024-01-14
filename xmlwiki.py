import requests
from bs4 import BeautifulSoup
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

google_credentials_path = 'credentials.json'

# Read the credentials.json file
with open(google_credentials_path, 'r') as file:
    creds_data = json.load(file)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Use the credentials to authorize the client
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
client = gspread.authorize(creds)

sheet_url = "https://docs.google.com/spreadsheets/d/189aTNkQt_XAhfshC9sA3ryvekaDnXt1pr7SKCh-jqOM/edit?usp=sharing"
spreadsheet = client.open_by_url(sheet_url)
worksheet = spreadsheet.get_worksheet(5) or spreadsheet.add_worksheet(title="Sheet4", rows="100", cols="20")

url = 'https://fortune.com/ranking/100-fastest-growing-companies/2023/search/'

response = requests.get(url)
rows = []
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
    script_content = script_tag.string
    data = json.loads(script_content)
    items = data.get('props').get('pageProps').get('franchiseList').get('items')
    for item in items:
        rank = item.get('rank')
        company_name = item.get('name')
        company_slug = item.get('slug')
        search_link = f'https://fortune.com/{company_slug}'
        another_response = requests.get(search_link)
        another_soup = BeautifulSoup(another_response.text, 'html.parser')
        another_script_tag = another_soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        another_script_content = another_script_tag.string
        another_data = json.loads(another_script_content)
        company_info = another_data.get('props').get('pageProps').get('franchiseListItem').get('companyInfo')
        print(company_info)
        company_link = company_info.get('Website')
        country = company_info.get('Country')
        headquaters = company_info.get('Headquarters')
        industry = company_info.get('Industry')
        CEO = company_info.get('CEO')
        url = company_info.get('Website')
        type = company_info.get('Company type')
        Ticker = company_info.get('Ticker')
        revenues = company_info.get('Revenues ($M)')
        profits = company_info.get('Profits ($M)')
        market = company_info.get('Market value ($M)')
        employees = company_info.get('Number of employees')
         
        record = [rank, company_name, country, headquaters, industry, CEO, url, type, Ticker, revenues, profits, market, employees]
        print(record)
        worksheet.append_row(record)

        rows.append(record)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
