"""
Конфигурация приложения.
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# ✅ Загружаем .env перед инициализацией
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    DB_POOL_SIZE: int = int(
        os.getenv("DB_POOL_SIZE", 10)
    )  # ✅ Добавляем значение по умолчанию
    DB_MAX_OVERFLOW: int = int(
        os.getenv("DB_MAX_OVERFLOW", 20)
    )  # ✅ Максимальный размер пула соединений

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

if settings.DEBUG:
    print("✅ DEBUG MODE ВКЛЮЧЕН!")

if not settings.DATABASE_URL:
    raise ValueError("❌ Ошибка: DATABASE_URL не найден в .env!")
