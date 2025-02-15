"""
Схемы для управления дополнительными соглашениями (Addendums).
"""

from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AddendumBase(BaseModel):
    addendum_number: str
    addendum_date: date
    additional_amount: Decimal
    description: str | None = None


class AddendumCreate(AddendumBase):
    pass


class AddendumResponse(AddendumBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True


if settings.DEBUG:
    logger.debug("Схемы Addendum загружены")
