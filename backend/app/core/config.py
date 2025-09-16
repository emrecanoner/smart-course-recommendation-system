"""
Application configuration settings using Pydantic Settings.
"""

import os
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


def _find_env_file() -> str:
    """Find .env file dynamically based on current working directory."""
    # Possible locations for .env file
    possible_paths = [
        ".env",  # Current directory
        "../.env",  # Parent directory (when running from backend/)
        "../../.env",  # Two levels up (when running from backend/app/)
        "../../../.env",  # Three levels up (when running from backend/app/core/)
    ]
    
    # Check each possible path
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If no .env file found, return the most likely location
    return ".env"


class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Project information
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    
    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS settings
    BACKEND_CORS_ORIGINS: str
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Assemble CORS origins from string or list."""
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            return ",".join(v)
        elif v is None or v == "":
            return ""
        return v
    
    # Allowed hosts for security
    ALLOWED_HOSTS: str
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        """Assemble allowed hosts from string or list."""
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            return ",".join(v)
        elif v is None or v == "":
            return ""
        return v
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from individual components."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Redis settings (for caching and session management)
    REDIS_URL: str
    
    # AI/ML settings
    MODEL_PATH: str
    RECOMMENDATION_BATCH_SIZE: int
    RECOMMENDATION_CACHE_TTL: int
    
    # Logging settings
    LOG_LEVEL: str
    
    # Development settings
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Course seeding settings
    SEED_DATA_ENABLED: bool
    SEED_COURSES_COUNT: int = 0  # 0 means load all courses
    USE_COURSE_DATASET: bool
    COURSE_DATASET_PATH: str
    
    class Config:
        """Pydantic configuration."""
        case_sensitive = True
        env_file = _find_env_file()
        extra = "ignore"


# Create global settings instance
settings = Settings()