from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, condecimal

PriceType = Annotated[
    condecimal(max_digits=10, decimal_places=2), "PriceField"
]  # ✅ Правильный вариант


class SpecificationBase(BaseModel):
    spec_number: str = Field(..., max_length=50)
    spec_date: date
    goods_description: str = Field(..., max_length=255)
    price: PriceType
    volume: int
    total_amount: PriceType


class SpecificationCreate(SpecificationBase):
    pass


class SpecificationResponse(SpecificationBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True
