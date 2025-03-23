from datetime import datetime, timedelta
from bson import ObjectId

mongo = None

def init_db(db_instance):
    global mongo
    mongo = db_instance
    return mongo


class AudioRecord:
    """Audio record model for MongoDB."""
    
    @staticmethod
    def create(username, overall_class, confidence, probabilities):
        """
        Create a new audio record.
        
        Args:
            username (str): Username of the user who owns this record
            overall_class (int): The predicted class (0, 1, or 2)
            confidence (float): Confidence score for the prediction
            probabilities (dict): Probabilities for each class
            
        Returns:
            dict: The created audio record document
        """
        # Get user ID
        user = mongo.db.users.find_one({"username": username})
        if not user:
            return None
            
        # Create record document
        record = {
            "user_id": user['_id'],
            "username": username,
            "timestamp": datetime.utcnow(),
            "overall_class": overall_class,
            "confidence": confidence,
            "probabilities": probabilities
        }
        
        # Insert record into database
        result = mongo.db.audio_records.insert_one(record)
        record['_id'] = result.inserted_id
        return record
    
    @staticmethod
    def get_user_history(username, days=30):
        """
        Get audio analysis history for a user.
        
        Args:
            username (str): Username to get history for
            days (int): Number of days to look back
            
        Returns:
            list: List of audio record documents
        """
        # Get user
        user = mongo.db.users.find_one({"username": username})
        if not user:
            return []
            
        # Calculate date for filtering
        date_limit = datetime.utcnow() - timedelta(days=days)
        
        # Get records
        cursor = mongo.db.audio_records.find({
            "user_id": user['_id'],
            "timestamp": {"$gte": date_limit}
        }).sort("timestamp", -1)  # Sort by timestamp descending (newest first)
        
        return list(cursor)
    
    @staticmethod
    def get_by_id(record_id, username=None):
        """
        Get a record by ID, optionally filtering by username.
        
        Args:
            record_id (str): Record ID to look up
            username (str, optional): Username to filter by
            
        Returns:
            dict: Record document or None if not found
        """
        query = {"_id": ObjectId(record_id)}
        
        if username:
            user = mongo.db.users.find_one({"username": username})
            if not user:
                return None
            query["user_id"] = user['_id']
        
        return mongo.db.audio_records.find_one(query)