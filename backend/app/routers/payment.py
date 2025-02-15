"""
Маршруты для управления платежами.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import PaymentResponse
from app.services.payment_service import get_payments
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoices/{invoice_id}/payments", tags=["Payments"])


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(invoice_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить список платежей для инвойса.
    """
    if settings.DEBUG:
        logger.debug("Получение списка платежей для инвойса %d", invoice_id)

    payments = await get_payments(db, invoice_id)

    if not payments:
        logger.warning("Платежи не найдены для инвойса %d", invoice_id)

    return payments
