import unittest
from unittest.mock import patch
from src.scraper import extract_text_from_html, count_keyword_occurrences, fetch_webpage
import requests

class TestScraper(unittest.TestCase):

    # Test cases for extract_text_from_html
    def test_extract_text_from_html_basic(self):
        """
        Test that extract_text_from_html function correctly extracts text from basic HTML.
        """
        html_content = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>This is a test page</h1>
            <p>Welcome to the web scraping tutorial.</p>
            <script>alert('This should not be included');</script>
        </body>
        </html>
        """
        expected_text = "Test Page This is a test page Welcome to the web scraping tutorial."
        extracted_text = extract_text_from_html(html_content)
        self.assertEqual(extracted_text, expected_text)

    def test_extract_text_from_html_with_empty(self):
        """
        Test extract_text_from_html with empty HTML content.
        """
        html_content = ""
        expected_text = ""
        extracted_text = extract_text_from_html(html_content)
        self.assertEqual(extracted_text, expected_text)

    def test_extract_text_from_html_with_scripts_and_styles(self):
        """
        Test extract_text_from_html ensures scripts and styles are removed.
        """
        html_content = """
        <html>
        <head>
            <style>body {background-color: yellow;}</style>
            <script>console.log('This should not be included');</script>
        </head>
        <body>
            <h1>Visible Text</h1>
            <p>This is a paragraph.</p>
        </body>
        </html>
        """
        expected_text = "Visible Text This is a paragraph."
        extracted_text = extract_text_from_html(html_content)
        self.assertEqual(extracted_text, expected_text)

    # Test cases for count_keyword_occurrences
    def test_count_keyword_occurrences_basic(self):
        """
        Test that count_keyword_occurrences function correctly counts whole-word matches.
        """
        text = "This is a test page. Welcome to the web scraping tutorial. Web scraping is fun."
        keywords = ["web", "scraping", "tutorial", "notfound"]

        expected_counts = {
            "web": 2,         # "web" appears twice
            "scraping": 2,    # "scraping" appears twice
            "tutorial": 1,    # "tutorial" appears once
            "notfound": 0     # "notfound" doesn't appear
        }

        keyword_counts = count_keyword_occurrences(text, keywords)
        self.assertEqual(keyword_counts, expected_counts)

    def test_count_keyword_occurrences_case_insensitivity(self):
        """
        Test that count_keyword_occurrences is case-insensitive.
        """
        text = "This is a Test. test TEST Testy testing."
        keywords = ["test"]

        expected_counts = {
            "test": 3  # "test" appears as "Test", "test", and "TEST", but not "Testy"
        }

        keyword_counts = count_keyword_occurrences(text, keywords)
        self.assertEqual(keyword_counts, expected_counts)

    def test_count_keyword_occurrences_no_keywords(self):
        """
        Test count_keyword_occurrences with an empty list of keywords.
        """
        text = "This is a test page."
        keywords = []

        expected_counts = {}

        keyword_counts = count_keyword_occurrences(text, keywords)
        self.assertEqual(keyword_counts, expected_counts)

    def test_count_keyword_occurrences_empty_text(self):
        """
        Test count_keyword_occurrences with an empty text string.
        """
        text = ""
        keywords = ["test", "example"]

        expected_counts = {
            "test": 0,
            "example": 0
        }

        keyword_counts = count_keyword_occurrences(text, keywords)
        self.assertEqual(keyword_counts, expected_counts)

    def test_count_keyword_occurrences_with_phrases(self):
        """
        Test count_keyword_occurrences for matching multi-word phrases.
        """
        text = "This is a web scraping test. Web scraping is fun."
        keywords = ["web scraping", "test"]

        expected_counts = {
            "web scraping": 2,  # "web scraping" appears twice
            "test": 1           # "test" appears once
        }

        keyword_counts = count_keyword_occurrences(text, keywords)
        self.assertEqual(keyword_counts, expected_counts)

    # Test cases for fetch_webpage (using mock)
    @patch('requests.get')
    def test_fetch_webpage_success(self, mock_get):
        """
        Test fetch_webpage with a valid URL that returns a successful response.
        """
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"

        result = fetch_webpage("http://example.com")
        self.assertEqual(result, "<html><body>Test content</body></html>")

    @patch('requests.get')
    def test_fetch_webpage_timeout(self, mock_get):
        """
        Test fetch_webpage that raises a timeout error.
        """
        mock_get.side_effect = requests.exceptions.Timeout

        result = fetch_webpage("http://example.com")
        self.assertIsNone(result)

    @patch('requests.get')
    def test_fetch_webpage_404_error(self, mock_get):
        """
        Test fetch_webpage with a 404 error.
        """
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        result = fetch_webpage("http://example.com")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
