from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings

# Global database instance
_client: AsyncIOMotorClient = None
_database = None

async def get_database():
    """Get database instance"""
    global _client, _database
    
    if _database is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongo_uri)
        _database = _client.mentalhealth_analysis
    
    return _database

async def close_database():
    """Close database connection"""
    global _client
    if _client:
        _client.close()