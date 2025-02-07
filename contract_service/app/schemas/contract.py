"""
Схемы для управления контрактами.
"""

from datetime import date
from typing import Annotated, Optional
from pydantic import BaseModel, Field, condecimal
from app.config import settings
import logging

logger = logging.getLogger(__name__)

PriceType = Annotated[condecimal(max_digits=10, decimal_places=2), "PriceField"]


class ContractBase(BaseModel):
    contract_number: str = Field(..., max_length=50)
    contract_date: date
    valid_date: Optional[date] = None
    place_of_signing: Optional[str] = None
    currency: str = "CNY"
    exchange_rate: Optional[PriceType] = None

    supplier_name: str = Field(..., max_length=255)
    supplier_representative: str = Field(..., max_length=255)
    supplier_address: str = Field(..., max_length=255)
    supplier_bank: str = Field(..., max_length=255)
    supplier_account: str = Field(..., max_length=50)

    buyer_name: str = Field(..., max_length=255)
    buyer_address: str = Field(..., max_length=255)
    buyer_bank: str = Field(..., max_length=255)
    buyer_account: str = Field(..., max_length=50)

    goods_name: str = Field(..., max_length=255)
    quantity: int
    price_per_unit: PriceType
    total_price: PriceType

    payment_date: date
    delivery_terms: str = Field(..., max_length=50)
    claim_period: int
    response_period: int

    class Config:
        from_attributes = True


class ContractCreate(ContractBase):
    """Использует `ContractBase`, но отдельно определяет ID при создании."""
    pass


class ContractResponse(ContractBase):
    id: int

    class Config:
        from_attributes = True


if settings.DEBUG:
    logger.debug("Схемы Contract загружены")
