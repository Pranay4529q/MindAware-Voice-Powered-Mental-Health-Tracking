import os
from functools import lru_cache
from typing import Dict, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings"""
    
    # App Configuration
    app_name: str = "Mental Health Analysis API"
    debug: bool = False
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_secret_key: str = "jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 2
    
    
    
    # File Upload
    allowed_extensions: List[str] = ["wav", "mp3", "ogg"]
    max_file_size: int = 16 * 1024 * 1024  # I want only upto 16MB
    
    # Model Configuration
    model_path: str = "model/best_model.pth"
    class_labels: Dict[int, str] = {
        0: "Minimal", 
        1: "Moderate", 
        2: "Severe"
    }
    
    # Audio Processing
    sample_rate: int = 16000
    segment_length: float = 1.0
    n_fft: int = 1024
    hop_length: int = 256
    win_length: int = 1024
    n_mels: int = 64
    d_shape: int = 64
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
