"""
Schema definitions for contract specifications.
"""

from typing import Optional
from pydantic import Field
from .common import PriceType, DateType, CurrencyEnum, BaseSchema, BaseResponseSchema


class SpecificationBase(BaseSchema):
    """Base schema for specification data."""

    spec_number: str = Field(
        ..., max_length=50, description="Unique specification number"
    )
    spec_date: DateType
    goods_description: str = Field(
        ..., max_length=1000, description="Detailed description of goods"
    )
    price: PriceType = Field(..., description="Price per unit")
    volume: int = Field(..., gt=0, description="Quantity of goods")
    total_amount: PriceType = Field(..., description="Total specification amount")
    notes: Optional[str] = Field(
        None, max_length=1000, description="Additional specification notes"
    )
    currency: CurrencyEnum = CurrencyEnum.CNY

    model_config = {
        "json_schema_extra": {
            "example": {
                "spec_number": "SPEC-2024-001",
                "spec_date": "2024-01-15",
                "goods_description": "Product A - Standard Edition",
                "price": "100.00",
                "volume": 100,
                "total_amount": "10000.00",
                "currency": "CNY",
            }
        }
    }


class SpecificationCreate(SpecificationBase):
    """Schema for creating a new specification."""

    contract_id: int = Field(..., description="Associated contract ID")


class SpecificationUpdate(SpecificationBase):
    """Schema for updating specification."""

    pass


class SpecificationResponse(SpecificationBase, BaseResponseSchema):
    """Schema for specification response including ID and relationships."""

    contract_id: int = Field(..., description="Associated contract ID")
