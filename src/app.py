from flask import Flask, request, jsonify
from scraper import fetch_webpage, extract_text_from_html, count_keyword_occurrences
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    keywords = data.get('keywords')

    if not url or not keywords:
        return jsonify({'error': 'Invalid input'}), 400

    html_content = fetch_webpage(url)
    if html_content:
        page_text = extract_text_from_html(html_content)
        keyword_counts = count_keyword_occurrences(page_text, keywords)
        return jsonify({'keyword_counts': keyword_counts}), 200

    return jsonify({'error': 'Failed to scrape the website'}), 500

if __name__ == "__main__":
    app.run(debug=True)

# lsof -i :5000
# kill -9 <PID>
# http://127.0.0.1:5000/