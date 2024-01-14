# Comprehensive Web Scraping and Data Management Toolkit: README

## Overview

This toolkit comprises three distinct Python scripts designed for web scraping and data management. Each script is tailored to scrape specific types of data from different websites, process it, and then save it to Google Sheets. This README provides a detailed guide on the setup, usage, and functionality of each script.

## Prerequisites

Before using this toolkit, ensure you have the following prerequisites:

1. **Python:** The scripts are written in Python. Ensure Python is installed on your machine.
2. **Libraries:** BeautifulSoup for web scraping, gspread and oauth2client for Google Sheets integration, requests for HTTP requests, and json for JSON manipulation.
   
   Install these libraries using pip:
   ```bash
   pip install beautifulsoup4 gspread oauth2client requests
   ```

3. **Google Service Account Credentials:** You need a Google Cloud Platform service account with permissions to access Google Sheets. Store the credentials in a file named `credentials.json`.

## Installation

1. **Clone the Repository:**
   Download or clone the toolkit's repository to your local machine.

2. **Install Dependencies:**
   Navigate to the toolkit's directory and install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set Up Google Sheets API:**
   - Create a service account in Google Cloud Platform.
   - Download the JSON credentials and place them in the toolkit directory as `credentials.json`.
   - Share your target Google Sheets with the service account email.

## Usage

### Script 1: Fortune 100 Fastest-Growing Companies Scraper

- **Purpose:** Scrapes data about the top 100 fastest-growing companies from Fortune's website and saves it to Google Sheets.
- **Execution:** Run `python script1.py`.
- **Output:** Data including rank, company name, country, headquarters, industry, CEO, etc., is saved in the specified Google Sheet.

### Script 2: Best Places to Work in San Francisco Scraper

- **Purpose:** Extracts company information from Built In San Francisco's website.
- **Execution:** Run `python script2.py`.
- **Output:** Data including company name, type, link, and location is saved in the specified Google Sheet.

### Script 3: Growjo 200 Fastest Growing Companies Scraper

- **Purpose:** Collects data from Growjo’s website about 200 fast-growing companies.
- **Execution:** Run `python script3.py`.
- **Output:** Data including ranking, company name, link, city, country, funding, etc., is saved in the specified Google Sheet.

## How It Works

Each script performs the following steps:

1. **Set Up Google Sheets Connection:** Uses `gspread` and Google service account credentials to connect to a specific Google Sheets document.
2. **Web Scraping:** Sends HTTP requests to targeted websites, parses HTML responses using `BeautifulSoup`, and extracts relevant data.
3. **Data Processing:** Formats and structures the extracted data.
4. **Saving Data:** Appends the processed data to the specified Google Sheets.

## Limitations

- The scripts are dependent on the structure of the web pages. Any changes in the web pages may require adjustments to the scraping logic.
- Google Sheets API has usage limits.
