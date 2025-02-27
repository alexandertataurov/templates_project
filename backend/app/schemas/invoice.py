"""
Schema definitions for contract invoices.
"""

from typing import Optional
from pydantic import Field
from .common import (
    PriceType,
    DateType,
    CurrencyEnum,
    StatusEnum,
    BaseSchema,
    BaseResponseSchema,
)


class InvoiceBase(BaseSchema):
    """Base schema for invoice data."""

    invoice_number: str = Field(..., max_length=50, description="Unique invoice number")
    invoice_date: DateType
    due_date: DateType
    total_amount: PriceType = Field(..., description="Total invoice amount")
    currency: CurrencyEnum = CurrencyEnum.CNY
    status: StatusEnum = StatusEnum.PENDING
    notes: Optional[str] = Field(
        None, max_length=1000, description="Additional invoice notes"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "invoice_number": "INV-2024-001",
                "invoice_date": "2024-01-15",
                "due_date": "2024-02-15",
                "total_amount": "10000.00",
                "currency": "CNY",
                "status": "pending",
            }
        }
    }


class InvoiceCreate(InvoiceBase):
    """Schema for creating a new invoice."""

    contract_id: int = Field(..., description="Associated contract ID")


class InvoiceUpdate(InvoiceBase):
    """Schema for updating invoice."""

    pass


class InvoiceResponse(InvoiceBase, BaseResponseSchema):
    """Schema for invoice response including ID and relationships."""

    contract_id: int = Field(..., description="Associated contract ID")
