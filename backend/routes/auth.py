from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Get user data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validate data
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Create user
    user = User.create(username, email, password)
    
    if not user:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    
    # Get user data
    username = data.get('username')
    password = data.get('password')
    
    # Validate data
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Verify user
    user = User.verify_password(username, password)
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generate token
    access_token = create_access_token(identity=username)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'username': username
    }), 200