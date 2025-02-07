"""
Маршруты для управления спецификациями.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.specification import SpecificationCreate, SpecificationResponse
from app.services.specification_service import (
    create_specification,
    delete_specification,
    get_contract_by_specification,
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/contracts/{contract_id}/specifications", tags=["Specifications"]
)


@router.post("/", response_model=SpecificationResponse)
async def create_new_specification(
    contract_id: int,
    specification: SpecificationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Создать новую спецификацию.
    """
    if settings.DEBUG:
        logger.debug("Создание новой спецификации для контракта %d", contract_id)

    return await create_specification(db, contract_id, specification)


@router.get("/contract/{specification_id}")
async def get_contract_by_specification_endpoint(
    specification_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Получить контракт по спецификации.
    """
    if settings.DEBUG:
        logger.debug("Запрос контракта по спецификации ID %d", specification_id)

    contract = await get_contract_by_specification(db, specification_id)
    if not contract:
        logger.warning("Контракт для спецификации %d не найден", specification_id)
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract


@router.delete("/{spec_id}", status_code=204)
async def remove_specification(
    contract_id: int, spec_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Удалить спецификацию.
    """
    if settings.DEBUG:
        logger.debug(
            "Удаление спецификации ID %d из контракта %d", spec_id, contract_id
        )

    contract = await get_contract_by_specification(db, spec_id)
    if not contract:
        logger.warning("Контракт не найден для удаления спецификации %d", spec_id)
        raise HTTPException(status_code=404, detail="Contract not found")

    if not await delete_specification(db, spec_id):
        logger.warning("Спецификация ID %d не найдена", spec_id)
        raise HTTPException(status_code=404, detail="Specification not found")
