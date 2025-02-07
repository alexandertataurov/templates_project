from datetime import date

from pydantic import BaseModel


class AppendixBase(BaseModel):
    appendix_number: str
    appendix_date: date
    description: str | None = None


class AppendixCreate(AppendixBase):
    pass


class AppendixResponse(AppendixBase):
    id: int
    contract_id: int

    class Config:
        from_attributes = True
