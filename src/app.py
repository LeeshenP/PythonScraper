from flask import Flask, render_template, request
from scraper import fetch_webpage, extract_text_from_html, count_keyword_occurrences

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        keywords = request.form['keywords'].split(',')

        # Fetch the webpage content
        html_content = fetch_webpage(url)
        if html_content:
            # Extract text from the HTML content
            page_text = extract_text_from_html(html_content)

            # Count keyword occurrences
            keyword_counts = count_keyword_occurrences(page_text, keywords)

            return render_template('index.html', keyword_counts=keyword_counts, url=url, keywords=keywords)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
# lsof -i :5000
# kill -9 <PID>
# http://127.0.0.1:5000/