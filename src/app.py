from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import re

from scraper import count_keyword_occurrences, extract_text_from_html, fetch_webpage

app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# URL validation regex
url_regex = re.compile(
    r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)

# User registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Hash password and create new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# User login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check user credentials
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT token
    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token': access_token}), 200

# Protected route example
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), 200

@app.route('/api/scrape', methods=['POST'])
@jwt_required()  # Ensure this route requires JWT authentication
def scrape():
    current_user = get_jwt_identity()  # This fetches the user identity (username)
    data = request.get_json()

    url = data.get('url')
    keywords = data.get('keywords')

    # URL and keyword validation (as before)
    if not url or not url_regex.match(url):
        return jsonify({'error': 'Invalid URL'}), 400

    if not keywords or not isinstance(keywords, list) or len(keywords) == 0:
        return jsonify({'error': 'Invalid keywords'}), 400

    # Fetch the webpage content (same logic as before)
    html_content = fetch_webpage(url)
    if not html_content:
        return jsonify({'error': 'Failed to scrape the website'}), 500

    # Extract text and count occurrences
    page_text = extract_text_from_html(html_content)
    keyword_counts = count_keyword_occurrences(page_text, keywords)

    return jsonify({'keyword_counts': keyword_counts}), 200

if __name__ == "__main__":
    app.run(debug=True)

# lsof -i :5000
# kill -9 <PID>
# http://127.0.0.1:5000/