"""
Модель шаблонов (Templates).
"""

import logging
from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Template(Base):
    """Модель шаблона документа."""

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    display_name = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    dynamic_fields = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user_id = Column(Integer, nullable=True)


if settings.DEBUG:
    logger.debug("Модель Template загружена")
