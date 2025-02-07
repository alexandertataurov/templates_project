"""
Базовая модель для всех таблиц базы данных.
"""

import logging
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from app.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Абстрактный базовый класс моделей."""

    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


if settings.DEBUG:
    logger.debug("Base Model загружен")
