from pydantic import BaseModel, Field, condecimal
from datetime import date
from typing import Optional, Annotated

PriceType = Annotated[condecimal(max_digits=10, decimal_places=2), "PriceField"]  # ✅ Правильный вариант


class ContractBase(BaseModel):
    contract_number: str = Field(..., max_length=50)
    contract_date: date
    valid_date: Optional[date] = None
    place_of_signing: Optional[str] = None
    currency: str = "CNY"
    exchange_rate: PriceType = None

    supplier_name: str = Field(..., max_length=255)
    supplier_representative: str = Field(..., max_length=255)
    supplier_address: str = Field(..., max_length=255)
    supplier_inn: Optional[str] = Field(None, max_length=50)
    supplier_bik: Optional[str] = Field(None, max_length=50)
    supplier_ogrn: Optional[str] = Field(None, max_length=50)
    supplier_bank: str = Field(..., max_length=255)
    supplier_swift: Optional[str] = Field(None, max_length=50)
    supplier_account: str = Field(..., max_length=50)

    buyer_name: str = Field(..., max_length=255)
    buyer_address: str = Field(..., max_length=255)
    buyer_bank: str = Field(..., max_length=255)
    buyer_swift: Optional[str] = Field(None, max_length=50)
    buyer_account: str = Field(..., max_length=50)
    buyer_tax_id: Optional[str] = Field(None, max_length=50)

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

class ContractCreate(BaseModel):
    name: str
    start_date: str
    end_date: str
    
class ContractResponse(BaseModel):
    id: int
    name: str
    start_date: str
    end_date: str

    class Config:
        orm_mode = True  # Это важно для работы с SQLAlchemy    