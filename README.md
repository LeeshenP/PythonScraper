# Python Web Scraper Script

## Overview
This script takes user input keywords and scrapes a given website to count the occurrences of these keywords. The results are displayed in the terminal.

## Requirements
- Python 3.x
- Libraries: requests, beautifulsoup4

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeeshenP/PythonScraper.git

2. Ensure needed dependecies & libraries are installed
   ```bash
   pip install -r requirements.txt

## Additional Notes
- At the moment there is no script test but one can be created using locally made static webpages for automated testing
- It is recommended to use a Python venv to ensure no library or dependecy conflicts with other projects
- Selenium could be used in place of beautifulsoup4 in order to work with a headless browser (drivers needed for Chrome, Edge, Firefox respectively)
  in order to better scrape JavaScript heavy websites.
