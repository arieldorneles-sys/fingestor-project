from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database - SQLite para desenvolvimento local
    DATABASE_URL: str = "sqlite:///./fingestor.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FinGestor API"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # External APIs
    RECEITA_WS_BASE_URL: str = "https://www.receitaws.com.br/v1"
    
    # File uploads
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"


settings = Settings()

