from datetime import datetime, timedelta
from bson import ObjectId
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_database

class AudioRecord:
    """Audio record model for MongoDB with async operations"""
    
    @staticmethod
    async def create(username: str, overall_class: int, confidence: float, probabilities: Dict) -> Optional[Dict]:
        """Create a new audio record"""
        
        db = await get_database()
        
        # Get user ID
        user = await db.users.find_one({"username": username})
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
        result = await db.audio_records.insert_one(record)
        record['_id'] = result.inserted_id
        return record
    
    @staticmethod
    async def get_user_history(username: str, days: int = 30) -> List[Dict]:
        """Get audio analysis history for a user"""
        
        db = await get_database()
        
        # Get user
        user = await db.users.find_one({"username": username})
        if not user:
            return []
            
        # Calculate date for filtering
        date_limit = datetime.utcnow() - timedelta(days=days)
        
        # Get records
        cursor = db.audio_records.find({
            "user_id": user['_id'],
            "timestamp": {"$gte": date_limit}
        }).sort("timestamp", -1)  # Sort by timestamp descending
        
        return await cursor.to_list(length=None)
    
    @staticmethod
    async def get_by_id(record_id: str, username: Optional[str] = None) -> Optional[Dict]:
        """Get a record by ID, optionally filtering by username"""
        
        db = await get_database()
        
        try:
            query = {"_id": ObjectId(record_id)}
            
            if username:
                user = await db.users.find_one({"username": username})
                if not user:
                    return None
                query["user_id"] = user['_id']
            
            return await db.audio_records.find_one(query)
            
        except Exception:
            return None