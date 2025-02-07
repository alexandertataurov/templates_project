"""
Маршруты для управления инвойсами.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceResponse
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts/{contract_id}/invoices", tags=["Invoices"])


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить список инвойсов для контракта."""
    if settings.DEBUG:
        logger.debug("Запрос инвойсов для контракта %d", contract_id)

    result = await db.execute(select(Invoice).where(Invoice.contract_id == contract_id))
    invoices = result.scalars().all()

    if not invoices:
        logger.warning("Инвойсы не найдены для контракта %d", contract_id)

    return invoices  # ✅ Возвращает [] вместо ошибки 404
