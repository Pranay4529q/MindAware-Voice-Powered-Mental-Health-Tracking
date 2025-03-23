from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User

# Create blueprint
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the current user's profile."""
    # Get current user
    username = get_jwt_identity()
    user = User.get_by_username(username)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Return user data (excluding password)
    return jsonify({
        'username': user['username'],
        'email': user['email'],
        'created_at': user['created_at']
    }), 200

@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the current user's profile."""
    # Get current user
    username = get_jwt_identity()
    
    # Get update data
    data = request.get_json()
    
    # Update user
    updated_user = User.update_profile(username, data)
    
    if not updated_user:
        return jsonify({'error': 'User not found or no changes made'}), 404
    
    # Return updated user data
    return jsonify({
        'message': 'Profile updated successfully',
        'username': updated_user['username'],
        'email': updated_user['email']
    }), 200