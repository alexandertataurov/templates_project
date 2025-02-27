"""
Schema definitions for contract addendums.
"""

from typing import Optional
from pydantic import Field
from .common import PriceType, DateType, CurrencyEnum, BaseSchema, BaseResponseSchema


class AddendumBase(BaseSchema):
    """Base schema for addendum data."""

    addendum_number: str = Field(
        ..., max_length=50, description="Unique addendum number"
    )
    addendum_date: DateType
    additional_amount: PriceType = Field(
        ..., description="Additional amount specified in the addendum"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Detailed description of changes"
    )
    currency: CurrencyEnum = CurrencyEnum.CNY

    model_config = {
        "json_schema_extra": {
            "example": {
                "addendum_number": "ADD-2024-001",
                "addendum_date": "2024-01-15",
                "additional_amount": "5000.00",
                "description": "Additional goods delivery",
            }
        }
    }


class AddendumCreate(AddendumBase):
    """Schema for creating a new addendum."""

    contract_id: int = Field(..., description="Associated contract ID")


class AddendumUpdate(AddendumBase):
    """Schema for updating addendum."""

    pass


class AddendumResponse(AddendumBase, BaseResponseSchema):
    """Schema for addendum response including ID and relationships."""

    contract_id: int = Field(..., description="Associated contract ID")
