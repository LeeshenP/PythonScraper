import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database and tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'

def test_register_duplicate_user(client):
    """Test registering a duplicate user"""
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    response = client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'User already exists'

def test_login_success(client):
    """Test successful login"""
    # First, register a new user
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    # Then, attempt to log in
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid credentials'
