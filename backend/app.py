import os
import torch
from flask import Flask
from flask_cors import CORS


from config import get_config


from model.load_model import load_model

def create_app(config_name='dev'):
    """Create and configure the Flask application."""
   
    app = Flask(__name__)
    
   
    app.config.from_object(get_config())
    
    
    app.config["MONGO_URI"] = "mongodb://localhost:27017/depression_analysis"
    app.config['JWT_SECRET_KEY'] = 'topsecret'
    
    CORS(app)
    
    from models import init_app as init_models
    init_models(app)
    
    from utils import init_app as init_utils
    init_utils(app)
    
    app.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        app.model = load_model(app.config['MODEL_PATH'], app.device)
        app.model.eval()  
        app.logger.info(f"Model loaded successfully from {app.config['MODEL_PATH']}")
    except Exception as e:
        app.logger.error(f"Failed to load model: {str(e)}")
    
    from routes import init_app as init_routes
    init_routes(app)
    
    return app

app = create_app()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    # Run app
    app.run(debug=app.config['DEBUG'])