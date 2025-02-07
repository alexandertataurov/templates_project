from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, condecimal

PriceType = Annotated[
    condecimal(max_digits=10, decimal_places=2), "PriceField"
]  # ✅ Правильный вариант


class InvoiceBase(BaseModel):
    invoice_number: str = Field(..., max_length=50)
    invoice_date: date
    due_date: date
    total_amount: PriceType
    currency: str = "CNY"
    status: str = Field("pending", max_length=20)


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceResponse(InvoiceBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True
