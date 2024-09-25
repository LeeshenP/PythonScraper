# Python Web Scraper Script

## Overview
This script takes user input keywords and scrapes a given website to count the occurrences of these keywords. The results are displayed in the terminal.

## Requirements
- Python 3.x
- Libraries: requests, beautifulsoup4, flask

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeeshenP/PythonScraper.git

2. Ensure needed dependecies & libraries are installed
   ```bash
   pip install -r requirements.txt

3. If using a virtual environment (recommended), activate it
   ```bash
   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate

## Running the Flask Back-end
   ```bash
   cd src/
   python app.py
```
## Running the React Front-end
   ```bash
   cd client/
   npm install
   npm start
```
## Ports Used
   -  React front-end will run on http://localhost:3000/
   -  Flask will run on http://127.0.0.1:5000/.

## Testing
- At the moment, there is a simple, manual test script that will be updated periodically to test:
   ```bash
   python -m unittest discover tests/

## Additional Notes
- It is recommended to use a Python venv to ensure no library or dependecy conflicts with other projects
- If there is port in use error when re-running the app please do the following
   ```bash
   lsof -i :5000
   # locate <PID>
   kill -9 <PID>
- Selenium could be used in place of beautifulsoup4 in order to work with a headless browser (drivers needed for Chrome, Edge, Firefox respectively)
  in order to better scrape JavaScript heavy websites.
