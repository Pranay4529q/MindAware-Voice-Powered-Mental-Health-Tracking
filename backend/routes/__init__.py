from flask import Blueprint

# Create a main blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

def init_app(app):
    """Initialize routes with the app."""
    # Import and register route blueprints
    from .auth import auth_bp
    from .profile import profile_bp
    from .audio import audio_bp
    
    # Register blueprints with the API blueprint
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(profile_bp)
    api_bp.register_blueprint(audio_bp)
    
    # Register the main API blueprint with the app
    app.register_blueprint(api_bp)