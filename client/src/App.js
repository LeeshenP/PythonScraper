import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const validateForm = () => {
    if (!url) {
      setError('Please enter a valid URL');
      return false;
    }

    if (!keywords || keywords.trim() === '') {
      setError('Please enter at least one keyword');
      return false;
    }

    // Simple URL validation (you can enhance this if needed)
    const urlPattern = new RegExp(
      '^(https?:\\/\\/)?' + // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|' + // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
      '(\\#[-a-z\\d_]*)?$', 'i' // fragment locator
    );
    
    if (!urlPattern.test(url)) {
      setError('Please enter a valid URL');
      return false;
    }

    return true;
  };

  const handleScrape = async (e) => {
    e.preventDefault();
    setError(''); // Clear any previous error
    setResults(null); // Clear previous results

    if (!validateForm()) {
      return; // Prevent submitting if form is invalid
    }

    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/scrape', {
        url,
        keywords: keywords.split(',').map(keyword => keyword.trim())
      });

      setResults(response.data.keyword_counts);
      setLoading(false);
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setError(error.response.data.error);
      } else if (error.response && error.response.status === 500) {
        setError('Server error: Failed to scrape the website. Please try again later.');
      } else {
        setError('An unknown error occurred. Please check your connection or try again later.');
      }
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
            type="text"  // Change type from 'url' to 'text' for custom validation
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter website URL"
          />
        </div>
        <div>
          <label>Keywords/Phrases:</label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="Enter keywords (comma-separated)"
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
