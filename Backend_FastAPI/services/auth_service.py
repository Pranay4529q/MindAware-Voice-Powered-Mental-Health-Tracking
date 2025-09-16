import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException, status

from core.config import get_settings

class AuthService:
    """Service for authentication operations"""
    
    def __init__(self):
        self.settings = get_settings()
    
    def generate_token(self, user_data: Dict) -> str:
        """Generate a JWT token for a user"""
        
        payload = {
            "sub": user_data.get("username"),  # subject
            "iat": datetime.utcnow(),  # issued at
            "exp": datetime.utcnow() + timedelta(hours=self.settings.jwt_expire_hours)
        }
        
        token = jwt.encode(
            payload, 
            self.settings.jwt_secret_key, 
            algorithm=self.settings.jwt_algorithm
        )
        
        return token
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token"""
        
        try:
            payload = jwt.decode(
                token, 
                self.settings.jwt_secret_key, 
                algorithms=[self.settings.jwt_algorithm]
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def get_current_user(self, token: str) -> str:
        """Get current user from token"""
        payload = self.verify_token(token)
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return username
    
    def hash_password(self, password: str) -> str:
        """Hasing a password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)