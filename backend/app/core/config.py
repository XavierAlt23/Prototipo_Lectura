"""
backend/app/core/config.py
Configuración centralizada
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Backend
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://cyberbullying_user:password@localhost:5432/cyberbullying_detection"
    )
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # ML
    MODEL_CHECKPOINT_DIR: str = os.getenv("MODEL_CHECKPOINT_DIR", "./ml/checkpoints")
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./.cache")
    DEVICE: str = os.getenv("DEVICE", "cpu")
    RANDOM_SEED: int = int(os.getenv("RANDOM_SEED", 42))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]
    
    # API
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()
