"""
Contract schema definitions.
"""

from typing import Optional
from pydantic import Field
from .common import PriceType, DateType, CurrencyEnum, BaseSchema, BaseResponseSchema


class ContractBase(BaseSchema):
    """Base schema for contract data."""

    # Contract details
    contract_number: str = Field(
        ..., max_length=50, description="Unique contract number"
    )
    contract_date: DateType
    valid_date: Optional[DateType] = None
    place_of_signing: str = Field(
        ..., max_length=255, description="Location where contract was signed"
    )
    currency: CurrencyEnum = CurrencyEnum.CNY
    exchange_rate: Optional[PriceType] = None

    # Supplier details
    supplier_name: str = Field(..., max_length=255)
    supplier_representative: str = Field(..., max_length=255)
    supplier_address: str = Field(..., max_length=255)
    supplier_bank: str = Field(..., max_length=255)
    supplier_account: str = Field(..., max_length=50)

    # Buyer details
    buyer_name: str = Field(..., max_length=255)
    buyer_address: str = Field(..., max_length=255)
    buyer_bank: str = Field(..., max_length=255)
    buyer_account: str = Field(..., max_length=50)

    # Goods details
    goods_name: str = Field(..., max_length=255)
    quantity: int = Field(..., gt=0)
    price_per_unit: PriceType
    total_price: PriceType

    # Terms
    payment_date: DateType
    delivery_terms: str = Field(..., max_length=50)
    claim_period: int = Field(..., gt=0)
    response_period: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "contract_number": "CNT-2024-001",
                "contract_date": "2024-01-01",
                "currency": "CNY",
                "supplier_name": "Example Supplier Ltd.",
                # ... other example values
            }
        }
    }


class ContractCreate(ContractBase):
    """Schema for creating a new contract."""

    pass


class ContractUpdate(ContractBase):
    """Schema for updating contract."""

    pass


class ContractResponse(ContractBase, BaseResponseSchema):
    """Schema for contract response including ID."""

    pass
