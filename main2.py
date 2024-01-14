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
worksheet = spreadsheet.get_worksheet(2) or spreadsheet.add_worksheet(title="Sheet3", rows="100", cols="20")

with open('content2.html', 'r', encoding='utf-8') as file:
    html_content = file.read()


# Parse HTML Content
soup = BeautifulSoup(html_content, 'html.parser')

rows = []

# Find all <tr> elements and then <td> elements within each <tr>
for div in soup.find_all("div", class_="wysiwyg-wrapper"):
    print(div)
    # Find all <td> elements within this <tr>
    titles = div.find_all('h4')
    details = div.find_all('ul')
    urls = div.find_all('p')
    for index, title in enumerate(titles):
        record = []
        record.append(titles[index].get_text().strip().replace("\n", " ").replace("  ", " "))
        record.append(details[index].find_all('li')[0].get_text().replace("\n", " ").replace("  ", " "))
        record.append(details[index].find_all('li')[1].get_text().replace("\n", " ").replace("  ", " "))
        record.append(details[index].find_all('li')[2].get_text().replace("\n", " ").replace("  ", " "))
        record.append(urls[index].find('a').get('href'))    
        rows.append(record)
    
worksheet.append_rows(rows)
