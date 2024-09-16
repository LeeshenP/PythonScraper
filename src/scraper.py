import re
import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retry settings
MAX_RETRIES = 3
TIMEOUT = 10  # seconds


def get_valid_url():
    """
    Prompt user to enter a valid website URL.
    Returns a valid URL string.
    """
    while True:
        url = input("Enter the website URL to scrape: ").strip()

        # Validate URL format using regex
        if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
            return url
        else:
            print("Invalid URL format. Please enter a valid URL.")
            logging.warning("Invalid URL entered by user.")


def get_valid_keywords():
    """
    Prompt user to enter valid keywords or phrases.
    Returns a list of keywords.
    """
    while True:
        keywords_input = input("Enter keywords or phrases to search, separated by commas: ").strip()

        # Split the input into a list of keywords/phrases and remove redundant spaces
        keywords = [keyword.strip() for keyword in keywords_input.split(',') if keyword.strip()]

        if keywords:
            return keywords
        else:
            print("No valid keywords or phrases entered. Please try again.")
            logging.warning("No valid keywords entered by user.")


def fetch_webpage(url):
    """
    Fetch the webpage content from the given URL.
    Implements retry and timeout logic to handle transient errors.
    Returns the raw HTML content of the page or None if it fails.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()  # Raise an error for bad status codes
            logging.info(f"Successfully fetched URL: {url}")
            return response.text
        except requests.exceptions.Timeout:
            retries += 1
            logging.warning(f"Timeout fetching URL {url}. Retrying {retries}/{MAX_RETRIES}...")
            time.sleep(1)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching URL: {url} - {e}")
            break  # Do not retry on non-timeout errors

    print(f"Failed to fetch the URL after {MAX_RETRIES} retries.")
    return None


def extract_text_from_html(html_content):
    """
    Extract readable text from the raw HTML content using BeautifulSoup.
    Returns a string containing all the text in the page.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove scripts, styles, and other irrelevant content
    for script in soup(["script", "style"]):
        script.decompose()

    # Get the readable text from the page
    text = soup.get_text(separator=' ')

    # Clean up and normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def count_keyword_occurrences(text, keywords):
    """
    Count the occurrences of each keyword as a whole word in the text.
    Returns a dictionary with keyword counts.
    """
    keyword_counts = {}
    for keyword in keywords:
        # Use regular expressions to count whole word occurrences (case-insensitive)
        pattern = rf'\b{re.escape(keyword)}\b'
        count = len(re.findall(pattern, text, flags=re.IGNORECASE))
        keyword_counts[keyword] = count
    return keyword_counts


if __name__ == "__main__":
    # Get valid URL and keywords
    url = get_valid_url()
    keywords = get_valid_keywords()

    # Fetch the webpage content
    html_content = fetch_webpage(url)
    if html_content:
        # Extract text from the HTML content
        page_text = extract_text_from_html(html_content)

        # Count the occurrences of each keyword
        keyword_counts = count_keyword_occurrences(page_text, keywords)

        # Output the keyword counts
        print(f"\nKeyword occurrences on {url}:")
        for keyword, count in keyword_counts.items():
            print(f"'{keyword}': {count} occurrence(s)")

        # Log the keyword counts
        logging.info(f"Keyword counts for URL {url}: {keyword_counts}")
