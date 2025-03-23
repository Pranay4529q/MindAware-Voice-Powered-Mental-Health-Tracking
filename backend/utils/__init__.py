from flask_jwt_extended import JWTManager

# Initialize JWT manager
jwt = JWTManager()

def init_app(app):
    """Initialize utilities with the app."""
    jwt.init_app(app)