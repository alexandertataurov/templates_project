"""
Маршруты для управления дополнительными соглашениями (Addendums).
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.addendum import AddendumCreate, AddendumResponse
from app.services.addendum_service import (
    create_addendum,
    delete_addendum,
    get_addendums,
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts/{contract_id}/addendums", tags=["Addendums"])


@router.post("/", response_model=AddendumResponse)
async def create_new_addendum(
    contract_id: int, addendum: AddendumCreate, db: AsyncSession = Depends(get_db)
):
    """Создать новое дополнительное соглашение."""
    if settings.DEBUG:
        logger.debug(
            "Создание нового дополнительного соглашения для контракта %d", contract_id
        )
    return await create_addendum(db, contract_id, addendum)


@router.get("/", response_model=List[AddendumResponse])
async def list_addendums(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить список дополнительных соглашений."""
    if settings.DEBUG:
        logger.debug(
            "Получение списка дополнительных соглашений для контракта %d", contract_id
        )
    return await get_addendums(db, contract_id)


@router.delete("/{addendum_id}", status_code=204)
async def remove_addendum(
    contract_id: int, addendum_id: int, db: AsyncSession = Depends(get_db)
):
    """Удалить дополнительное соглашение."""
    if settings.DEBUG:
        logger.debug(
            "Удаление дополнительного соглашения ID: %d из контракта %d",
            addendum_id,
            contract_id,
        )

    if not await delete_addendum(db, addendum_id):
        logger.warning("Дополнительное соглашение ID: %d не найдено", addendum_id)
        raise HTTPException(status_code=404, detail="Addendum not found")
