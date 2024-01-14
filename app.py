import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

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
worksheet = spreadsheet.get_worksheet(4) or spreadsheet.add_worksheet(title="Sheet4", rows="100", cols="20")

for i in range(1,276):
    url = f'https://www.builtinsf.com/companies/best-places-to-work-san_francisco-2021?page={276}'

    response = requests.get(url)
    rows = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.find_all('div', class_='company-unbounded-responsive')
        for content in contents:
            links = content.find_all('a')
            if len(links) >= 5:
                company_name = links[4].text
                company_type = content.find('div', class_='font-barlow fw-medium text-gray-04 mb-sm').text
                company_link = links[4].get('href')
                company_location = content.find('span', class_='text-gray-03').text                
                record = [company_name, company_type, company_link, company_location]
                print(record)
                rows.append(record)
            else:
                print("Error: Not enough links on this page. Going to the next page.")
                break
        worksheet.append_rows(rows)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
