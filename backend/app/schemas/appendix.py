"""
Схемы для управления приложениями (Appendices).
"""

from datetime import date
from pydantic import BaseModel, Field
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AppendixBase(BaseModel):
    appendix_number: str = Field(..., max_length=50)
    appendix_date: date
    description: str | None = None


class AppendixCreate(AppendixBase):
    pass


class AppendixResponse(AppendixBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True


if settings.DEBUG:
    logger.debug("Схемы Appendix загружены")
