from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

mongo = None

# def init_db(app):
#     global mongo
#     mongo = PyMongo(app)
#     return mongo
def init_db(mongo_instance):
    global mongo
    mongo = mongo_instance
    return mongo


class User:
    """User model for MongoDB."""
    
    @staticmethod
    def create(username, email, password):
        """
        Create a new user.
        
        Args:
            username (str): Username for the new user
            email (str): Email address for the new user
            password (str): Password for the new user
            
        Returns:
            dict: The created user document or None if username/email already exists
        """
        # Check if user already exists
        if mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
            return None
        
        # Create user document
        user = {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "created_at": datetime.utcnow()
        }
        
        # Insert user into database
        mongo.db.users.insert_one(user)
        return user
    
    @staticmethod
    def get_by_username(username):
        """
        Get user by username.
        
        Args:
            username (str): Username to look up
            
        Returns:
            dict: User document or None if not found
        """
        return mongo.db.users.find_one({"username": username})
    
    @staticmethod
    def get_by_id(user_id):
        """
        Get user by ID.
        
        Args:
            user_id (str): User ID to look up
            
        Returns:
            dict: User document or None if not found
        """
        return mongo.db.users.find_one({"_id": user_id})
    
    @staticmethod
    def verify_password(username, password):
        """
        Verify password for a user.
        
        Args:
            username (str): Username to verify
            password (str): Password to verify
            
        Returns:
            dict: User document if verification successful, None otherwise
        """
        user = User.get_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def update_profile(username, update_data):
        """
        Update user profile.
        
        Args:
            username (str): Username of user to update
            update_data (dict): Data to update
            
        Returns:
            dict: Updated user document or None if user not found
        """
        # Don't allow updating username or password through this method
        safe_updates = {k: v for k, v in update_data.items() if k not in ['username', 'password']}
        
        if safe_updates:
            result = mongo.db.users.update_one(
                {"username": username}, 
                {"$set": safe_updates}
            )
            
            if result.modified_count:
                return mongo.db.users.find_one({"username": username})
        
        return None