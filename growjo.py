import requests
from bs4 import BeautifulSoup
import re
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
worksheet = spreadsheet.get_worksheet(3) or spreadsheet.add_worksheet(title="Sheet4", rows="100", cols="20")



for i in range(1, 200):
    url = f'https://growjo.com/home/200'
    rows = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', string=re.compile(r'window.InitialData', re.DOTALL))
        if script_tag:
            match = re.search(r'window\.InitialData', script_tag.text, re.DOTALL)
            if match:
                data_content = match.string
                cleaned_string = data_content.replace('window.InitialData = ', '')
                data = json.loads(cleaned_string)
                items = data.get('data')
                for item in items:
                    ranking = item.get('ranking')
                    company_name = item.get('company_name')
                    company_link = "https://www." + str(item.get('url'))
                    city = item.get('city', '')
                    country = item.get('country', '')
                    funding = item.get('total_funding', '')
                    industry = item.get('Industry', '')
                    employees = item.get('current_employees', '')
                    revenues = item.get('estimated_revenues', '')
                    growth = item.get('employee_growth', '')     
                    record = [ranking, company_name, company_link, city, country, "$" + str(funding), industry, employees, "$" + str(revenues), str(growth) + "%"]             
                    print(record)
                    rows.append(record)
                worksheet.append_rows(rows)
            else:
                print("No valid data found within window.initialdata assignment.")
        else:
            print("No script tag with window.initialdata found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


