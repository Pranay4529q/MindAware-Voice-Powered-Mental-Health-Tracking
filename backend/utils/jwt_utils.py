from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

jwt = JWTManager()

def init_jwt(app):
    """Initialize JWT with the app."""
    jwt.init_app(app)
    return jwt

def generate_token(user_data):
    """
    Generate a JWT token for a user.
    
    Args:
        user_data (dict): User data to encode in the token
        
    Returns:
        str: JWT token
    """
    # We'll use username as the identity
    identity = user_data.get('username')
    
    # Create the token
    access_token = create_access_token(identity=identity)
    
    return access_token

def get_current_user():
    """
    Get the current user from the JWT token.
    
    Returns:
        str: Username of the current user
    """
    return get_jwt_identity()