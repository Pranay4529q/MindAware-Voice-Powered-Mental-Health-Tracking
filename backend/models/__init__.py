from flask_pymongo import PyMongo

# Create a shared database instance
mongo = PyMongo()

def init_app(app):
    """Initialize database and models with the app."""
    mongo.init_app(app)
    
    # Initialize models with the shared database instance
    from .user import init_db as init_user_db
    from .audio_record import init_db as init_audio_record_db
    
    init_user_db(mongo)
    init_audio_record_db(mongo)