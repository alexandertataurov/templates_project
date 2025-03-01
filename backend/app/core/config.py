"""
Application configuration management.
"""

import os
import logging
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load .env explicitly from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")
logger.debug("Loading .env from: %s", ENV_FILE_PATH)
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)


class Settings(BaseSettings):
    """Application settings."""

    # Application
    project_name: str = "Document Management API"
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str  # Required
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    DATABASE_URL: str  # Required
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_NAME: str = "contracts_db"

    # CORS
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = "logs.txt"

    # File Storage
    upload_dir: str = "uploads"
    max_upload_size: int = 5_242_880  # 5MB
    allowed_extensions: List[str] = ["pdf", "docx", "xlsx"]

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    def validate_DATABASE_URL(self) -> None:
        """Validate database URL format."""
        if not self.DATABASE_URL.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")

    def __init__(self, **kwargs):
        logger.debug(
            "Env vars before init: SECRET_KEY=%s, DATABASE_URL=%s",
            (
                os.getenv("SECRET_KEY")[:4] + "..."
                if os.getenv("SECRET_KEY")
                else "Not set"
            ),
            os.getenv("DATABASE_URL"),
        )
        super().__init__(**kwargs)
        self.validate_DATABASE_URL()
        logger.debug(
            "Settings initialized: debug=%s, DATABASE_URL=%s, SECRET_KEY=%s",
            self.DEBUG,
            self.DATABASE_URL,
            self.SECRET_KEY[:4] + "..." if self.SECRET_KEY else None,
        )


def get_settings() -> Settings:
    """Get settings instance without caching."""
    return Settings()


# Export settings instance
settings = get_settings()
logger.info("Application settings initialized")

if settings.DEBUG:
    print("✅ Режим отладки включен!")
