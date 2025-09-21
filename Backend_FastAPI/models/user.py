# from datetime import datetime
# from typing import Dict, Optional
# from passlib.context import CryptContext

# from database import get_database

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class User:
#     """User model for MongoDB with async operations"""
    
#     @staticmethod
#     async def create(username: str, email: str, password: str) -> Optional[Dict]:
#         """Create a new user"""
        
#         db = await get_database()
        
#         # Check if user already exists
#         existing_user = await db.users.find_one(
#             {"$or": [{"username": username}, {"email": email}]}
#         )
#         if existing_user:
#             return None
        
#         # Create user document
#         user = {
#             "username": username,
#             "email": email,
#             "password": pwd_context.hash(password),
#             "created_at": datetime.utcnow()
#         }
        
#         # Insert user into database
#         result = await db.users.insert_one(user)
#         user['_id'] = result.inserted_id
#         return user
    
#     @staticmethod
#     async def get_by_username(username: str) -> Optional[Dict]:
#         """Get user by username"""
        
#         db = await get_database()
#         return await db.users.find_one({"username": username})
    
#     @staticmethod
#     async def get_by_id(user_id: str) -> Optional[Dict]:
#         """Get user by ID"""
        
#         db = await get_database()
#         from bson import ObjectId
        
#         try:
#             return await db.users.find_one({"_id": ObjectId(user_id)})
#         except Exception:
#             return None
    
#     @staticmethod
#     async def verify_password(username: str, password: str) -> Optional[Dict]:
#         """Verify password for a user"""
        
#         user = await User.get_by_username(username)
#         if user and pwd_context.verify(password, user['password']):
#             return user
#         return None
    
#     @staticmethod
#     async def update_profile(username: str, update_data: Dict) -> Optional[Dict]:
#         """Update user profile"""
        
#         db = await get_database()
        
#         # Don't allow updating username or password through this method
#         safe_updates = {
#             k: v for k, v in update_data.items() 
#             if k not in ['username', 'password']
#         }
        
#         if safe_updates:
#             result = await db.users.update_one(
#                 {"username": username}, 
#                 {"$set": safe_updates}
#             )
            
#             if result.modified_count:
#                 return await db.users.find_one({"username": username})
        
#         return None
from datetime import datetime
from typing import Dict, Optional
from passlib.context import CryptContext
import bcrypt

from database import get_database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    """User model for MongoDB with async operations"""
    
    @staticmethod
    async def create(username: str, email: str, password: str) -> Optional[Dict]:
        """Create a new user"""
        
        db = await get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one(
            {"$or": [{"username": username}, {"email": email}]}
        )
        if existing_user:
            return None
        
        # Create user document
        user = {
            "username": username,
            "email": email,
            "password": pwd_context.hash(password),
            "created_at": datetime.utcnow()
        }
        
        # Insert user into database
        result = await db.users.insert_one(user)
        user['_id'] = result.inserted_id
        return user
    
    @staticmethod
    async def get_by_username(username: str) -> Optional[Dict]:
        """Get user by username"""
        
        db = await get_database()
        return await db.users.find_one({"username": username})
    
    @staticmethod
    async def get_by_id(user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        
        db = await get_database()
        from bson import ObjectId
        
        try:
            return await db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
    
    @staticmethod
    async def verify_password(username: str, password: str) -> Optional[Dict]:
        """Verify password for a user"""
        
        user = await User.get_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None
    
    @staticmethod
    async def update_profile(username: str, update_data: Dict) -> Optional[Dict]:
        """Update user profile"""
        
        db = await get_database()
        
        # Don't allow updating username or password through this method
        safe_updates = {
            k: v for k, v in update_data.items() 
            if k not in ['username', 'password']
        }
        
        if safe_updates:
            result = await db.users.update_one(
                {"username": username}, 
                {"$set": safe_updates}
            )
            
            if result.modified_count:
                return await db.users.find_one({"username": username})
        
        return None