from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceResponse
from typing import List

router = APIRouter(prefix="/contracts/{contract_id}/invoices", tags=["Invoices"])

@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить список инвойсов для контракта"""
    result = await db.execute(select(Invoice).where(Invoice.contract_id == contract_id))
    return result.scalars().all()  # ✅ Возвращает [] вместо ошибки 404
