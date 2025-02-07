"""
Маршруты для получения статистики.
"""

import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.stats_service import get_monthly_stats, get_total_addendum_amount, get_total_contract_amount
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/total-contracts")
async def total_contracts(db: AsyncSession = Depends(get_db)):
    """Получить общую сумму контрактов."""
    if settings.DEBUG:
        logger.debug("Запрос общей суммы контрактов")
    return {"total_contract_amount": await get_total_contract_amount(db)}


@router.get("/total-addendums")
async def total_addendums(db: AsyncSession = Depends(get_db)):
    """Получить общую сумму дополнительных соглашений."""
    if settings.DEBUG:
        logger.debug("Запрос общей суммы дополнительных соглашений")
    return {"total_addendum_amount": await get_total_addendum_amount(db)}
