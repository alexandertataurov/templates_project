"""
Схемы для управления платежами.
"""

from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field, condecimal
from app.config import settings
import logging

logger = logging.getLogger(__name__)

PriceType = Annotated[condecimal(max_digits=10, decimal_places=2), "PriceField"]


class PaymentBase(BaseModel):
    payment_date: date
    amount: PriceType
    currency: str = "CNY"
    payment_method: str = Field(..., max_length=50)
    status: str = Field("completed", max_length=20)


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    invoice_id: int

    class Config:
        from_attributes = True


if settings.DEBUG:
    logger.debug("Схемы Payment загружены")
