"""
Конфигурация приложения.

Загружает настройки из `.env` и предоставляет объект `settings` для доступа к переменным.
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  # Загружаем переменные окружения

class Settings(BaseSettings):
    """
    Класс для загрузки настроек из `.env`.
    """

    DATABASE_URL: str
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))

    class Config:
        env_file = ".env"

settings = Settings()
