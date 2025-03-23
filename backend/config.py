import os
import datetime

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mental_health_app')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    
    # Audio Processing Configuration
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    
    # Model Configuration
    MODEL_PATH = os.path.join('model', 'best_model.pth')
    
    # Class Labels
    CLASS_LABELS = {0: "Class 0", 1: "Class 1", 2: "Class 2"}
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, ensure to set these environment variables with secure values
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')


# Configuration dictionary
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}

# Default to development config
def get_config():
    env = os.environ.get('FLASK_ENV', 'dev')
    return config_by_name.get(env, DevelopmentConfig)