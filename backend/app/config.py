"""
Application configuration using Pydantic for environment variable validation.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation."""

    # Database settings
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_NAME: str = "contracts_db"

    # Application settings
    DEBUG: bool = False
    LOG_FILE: str = "logs.txt"
    LOG_LEVEL: str = "INFO"

    # Security settings
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # File storage settings
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="allow"
    )

    def validate_database_url(self) -> None:
        """Validate database URL format."""
        if not self.DATABASE_URL.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")


@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings instance."""
    settings = Settings()
    settings.validate_database_url()
    return settings


# Export settings instance
settings = get_settings()

if settings.DEBUG:
    print("✅ Режим отладки включен!")
