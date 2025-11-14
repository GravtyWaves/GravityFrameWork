"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Auth Service"
    debug: bool = False
    log_level: str = "INFO"
    
    # Service
    service_host: str = "0.0.0.0"
    service_port: int = 8001
    
    # Database (auto-injected by Gravity Framework)
    database_url: str
    
    # Redis (auto-injected by Gravity Framework)
    redis_url: str
    
    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  # 1 hour
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Session
    session_expiration: int = 86400  # 24 hours
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
