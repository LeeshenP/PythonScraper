import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleScrape = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/scrape', {
        url,
        keywords: keywords.split(',').map(keyword => keyword.trim())
      });
      setResults(response.data.keyword_counts);
      setLoading(false);
    } catch (error) {
      setError('Failed to scrape the website. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Keyword Scraper</h1>
      <form onSubmit={handleScrape}>
        <div>
          <label>Site to be Scraped:</label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter website URL"
            required
          />
        </div>
        <div>
          <label>Keywords/Phrases:</label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="Enter keywords (comma-separated)"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Scraping...' : 'Scrape Website'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results && (
        <div>
          <h2>Results:</h2>
          <ul>
            {Object.entries(results).map(([keyword, count]) => (
              <li key={keyword}>{keyword}: {count}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
