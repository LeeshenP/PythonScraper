import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import fetch_webpage, extract_text_from_html, count_keyword_occurrences
import re

app = Flask(__name__)
CORS(app)

# Setup logging to a file
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s')

# URL validation regex
url_regex = re.compile(
    r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()

        url = data.get('url')
        keywords = data.get('keywords')

        # Validate URL
        if not url or not url_regex.match(url):
            return jsonify({'error': 'Invalid URL'}), 400

        # Validate keywords
        if not keywords or not isinstance(keywords, list) or len(keywords) == 0:
            return jsonify({'error': 'Invalid keywords'}), 400

        # Fetch the webpage content
        html_content = fetch_webpage(url)
        if not html_content:
            return jsonify({'error': 'Failed to scrape the website'}), 500

        # Extract text and count occurrences
        page_text = extract_text_from_html(html_content)
        keyword_counts = count_keyword_occurrences(page_text, keywords)

        return jsonify({'keyword_counts': keyword_counts}), 200

    except Exception as e:
        # Log the exception
        logging.error(f"Error occurred while scraping: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True)

# lsof -i :5000
# kill -9 <PID>
# http://127.0.0.1:5000/