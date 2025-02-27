"""
Схемы для управления платежами.
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Optional
from pydantic import BaseModel, Field, condecimal
from app.config import settings
import logging

logger = logging.getLogger(__name__)

PriceType = Annotated[condecimal(max_digits=10, decimal_places=2), "PriceField"]


class PaymentMethodEnum(str, Enum):
    """Supported payment methods."""

    BANK_TRANSFER = "bank_transfer"
    WIRE = "wire"
    CHECK = "check"
    CASH = "cash"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentBase(BaseModel):
    payment_date: date
    amount: PriceType
    currency: str = "CNY"
    payment_method: PaymentMethodEnum
    status: str = Field("completed", max_length=20)
    reference: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    invoice_id: int


class PaymentUpdate(PaymentBase):
    """Schema for updating payment."""

    pass


class PaymentResponse(PaymentBase):
    id: int
    invoice_id: int

    class Config:
        from_attributes = True


if settings.DEBUG:
    logger.debug("Схемы Payment загружены")
