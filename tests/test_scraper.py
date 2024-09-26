import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_scrape_valid(client):
    """Test scraping with valid data"""
    # Register and log in a user
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Test scraping with valid data
    response = client.post('/api/scrape', json={
        'url': 'https://example.com',
        'keywords': ['example', 'test']
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'keyword_counts' in response.json

def test_scrape_invalid_url(client):
    """Test scraping with invalid URL"""
    # Register and log in a user
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Test scraping with an invalid URL
    response = client.post('/api/scrape', json={
        'url': 'invalid-url',
        'keywords': ['test']
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid URL'

def test_scrape_missing_keywords(client):
    """Test scraping with missing keywords"""
    # Register and log in a user
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Test scraping with missing keywords
    response = client.post('/api/scrape', json={
        'url': 'https://example.com',
        'keywords': []
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid keywords'
