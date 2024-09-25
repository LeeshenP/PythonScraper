import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [registerUsername, setRegisterUsername] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Scraper-related states
  const [url, setUrl] = useState('');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);  // Track loading state

  // Registration
  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/register', {
        username: registerUsername,
        password: registerPassword,
      });

      setMessage('User registered successfully. Please log in.');
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Registration failed');
    }
  };

  // Login
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        username: loginUsername,
        password: loginPassword,
      });

      const { access_token } = response.data;
      setToken(access_token);
      setIsAuthenticated(true);
      setMessage('Logged in successfully');
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Login failed');
    }
  };

  // Log Out
  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken('');
    setLoginUsername('');
    setLoginPassword('');
    setUrl('');
    setKeywords('');
    setResults(null);
    setMessage('Logged out successfully.');
  };

  // Scraping functionality
  const handleScrape = async (e) => {
    e.preventDefault();
    setError('');
    setResults(null);
    setLoading(true);  // Set loading state to true

    // Ensure keywords are provided
    if (!keywords || keywords.trim() === '') {
      setError('Please enter at least one keyword.');
      setLoading(false);  // Stop loading
      return;
    }

    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/api/scrape',
        {
          url,
          keywords: keywords.split(',').map((keyword) => keyword.trim()),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,  // Send JWT token in header
          },
        }
      );

      setResults(response.data.keyword_counts);
      setLoading(false);  // Set loading state to false after success
    } catch (error) {
      setError('Scraping failed. Please try again.');
      setLoading(false);  // Stop loading on error
    }
  };

  return (
    <div className="App">
      <h1>User Authentication and Scraper</h1>

      {!isAuthenticated ? (
        <>
          {/* Registration Form */}
          <form onSubmit={handleRegister}>
            <h2>Register</h2>
            <input
              type="text"
              placeholder="Username"
              value={registerUsername}
              onChange={(e) => setRegisterUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={registerPassword}
              onChange={(e) => setRegisterPassword(e.target.value)}
            />
            <button type="submit">Register</button>
          </form>

          {/* Login Form */}
          <form onSubmit={handleLogin}>
            <h2>Login</h2>
            <input
              type="text"
              placeholder="Username"
              value={loginUsername}
              onChange={(e) => setLoginUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
            />
            <button type="submit">Login</button>
          </form>
        </>
      ) : (
        <div>
          <h2>Welcome, {loginUsername}!</h2>

          {/* Scraper Form */}
          <form onSubmit={handleScrape}>
            <div>
              <label>Site to be Scraped:</label>
              <input
                type="text"
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

          {/* Display loading spinner while loading */}
          {loading && <div className="spinner"></div>}

          {/* Log Out Button */}
          <button onClick={handleLogout}>Log Out</button>

          {/* Display results */}
          {results && (
            <div>
              <h2>Results:</h2>
              <ul>
                {Object.entries(results).map(([keyword, count]) => (
                  <li key={keyword}>
                    {keyword}: {count}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Display error and success messages */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
    </div>
  );
}

export default App;
