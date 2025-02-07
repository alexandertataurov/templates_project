"""
Маршруты для управления приложениями (Appendices).
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.appendix import AppendixCreate, AppendixResponse
from app.services.appendix_service import create_appendix, delete_appendix, get_appendices
from app.config import settings  # ✅ Добавлен Debug Mode

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts/{contract_id}/appendices", tags=["Appendices"])


@router.post("/", response_model=AppendixResponse)
async def create_new_appendix(contract_id: int, appendix: AppendixCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новое приложение.
    """
    if settings.DEBUG:
        logger.debug("Создание нового приложения для контракта %d", contract_id)
    return await create_appendix(db, contract_id, appendix)


@router.get("/", response_model=List[AppendixResponse])
async def list_appendices(contract_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить список приложений.
    """
    if settings.DEBUG:
        logger.debug("Получение списка приложений для контракта %d", contract_id)
    return await get_appendices(db, contract_id)


@router.delete("/{appendix_id}", status_code=204)
async def remove_appendix(contract_id: int, appendix_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить приложение.
    """
    if settings.DEBUG:
        logger.debug("Удаление приложения ID: %d из контракта %d", appendix_id, contract_id)

    if not await delete_appendix(db, appendix_id):
        logger.warning("Приложение ID: %d не найдено", appendix_id)
        raise HTTPException(status_code=404, detail="Appendix not found")
