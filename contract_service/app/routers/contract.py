"""
Маршруты для управления контрактами.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractResponse
from app.services.contract_service import create_contract, get_contract
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/", response_model=ContractResponse)
async def create_new_contract(contract: ContractCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый контракт."""
    if settings.DEBUG:
        logger.debug("Создание нового контракта: %s", contract)
    return await create_contract(db, contract)


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract_detail(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить детали контракта."""
    if settings.DEBUG:
        logger.debug("Запрос деталей контракта %d", contract_id)

    contract = await get_contract(db, contract_id)
    if not contract:
        logger.warning("Контракт %d не найден", contract_id)
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract
