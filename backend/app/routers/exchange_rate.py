"""
Маршруты для управления курсами обмена валют.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.exchange_rate_service import update_contract_exchange_rate
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exchange-rate", tags=["Exchange Rate"])


@router.put("/contract/{contract_id}")
async def update_contract_rate(
    contract_id: int, new_rate: float, db: AsyncSession = Depends(get_db)
):
    """
    Обновить курс валюты в контракте.
    """
    if settings.DEBUG:
        logger.debug(
            "Обновление курса валюты для контракта %d, новый курс: %f",
            contract_id,
            new_rate,
        )

    if new_rate <= 0:
        logger.warning("Попытка установить некорректный курс: %f", new_rate)
        raise HTTPException(status_code=400, detail="Exchange rate must be positive")

    contract = await update_contract_exchange_rate(db, contract_id, new_rate)
    if not contract:
        logger.warning("Контракт %d не найден", contract_id)
        raise HTTPException(status_code=404, detail="Contract not found")

    return {"contract_id": contract_id, "new_exchange_rate": new_rate}
