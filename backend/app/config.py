"""Application configuration"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///C:/Users/noahs/Desktop/ETHHHH2026/StudyFlow/backend/studyflow.db"


    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "StudyFlow"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
