from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from deloitte import content  # Importing the HTML content from html_data.py

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
worksheet = spreadsheet.get_worksheet(6) or spreadsheet.add_worksheet(title="Sheet3", rows="100", cols="20")

with open('content3.html', 'r', encoding='utf-8') as file:
    html_content = file.read()


# Parse HTML Content
soup = BeautifulSoup(html_content, 'html.parser')

rows = []

# Find all <tr> elements and then <td> elements within each <tr>
for li in soup.find_all("li", class_='element'):
    # Find all <td> elements within this <tr>
    title = li.find('h2').text.replace('\n', ' ').replace('  ', '')
    url = li.find('a', {'rel': 'nofollow noopener noreferrer'}).text.replace('\n', ' ').replace('  ', '')    
    employees = li.find('dd', class_='text-gray-800').text.replace('\n', ' ').replace('  ', '')
    location = li.find('dd', class_='locations').text.replace('\n', ' ').replace('  ', '')
    record = [title, url, location, employees]
    rows.append(record)
    
worksheet.append_rows(rows)
