"""
Маршруты для получения статистики.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.stats_service import get_monthly_stats, get_total_amount_by_type
from app.core.config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/total/{document_type}")
async def total_by_type(document_type: str, db: AsyncSession = Depends(get_db)):
    """Получить общую сумму по типу документа."""
    if Settings.DEBUG:
        logger.debug("Запрос общей суммы для типа документа: %s", document_type)
    return {"total_amount": await get_total_amount_by_type(db, document_type)}


@router.get("/monthly/{year}/{month}")
async def monthly_stats(year: int, month: int, db: AsyncSession = Depends(get_db)):
    """Получить статистику за месяц."""
    if Settings.DEBUG:
        logger.debug("Запрос месячной статистики за %d-%d", year, month)
    return await get_monthly_stats(db, year, month)
