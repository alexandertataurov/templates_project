"""
Настройка подключения к базе данных.
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Настройка логирования
logger = logging.getLogger(__name__)

try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
    )
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def get_db():
        """
        Получает сессию базы данных.
        """
        async with async_session() as session:
            yield session

except Exception as e:
    logger.error("Ошибка подключения к базе данных: %s", e)
    raise
