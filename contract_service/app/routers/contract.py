from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.contract_service import create_contract, get_contracts, get_contract, delete_contract
from app.schemas.contract import ContractCreate, ContractResponse
from app.models.contract import Contract
from typing import List, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/", response_model=ContractResponse)
async def create_new_contract(contract: ContractCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый контракт"""
    return await create_contract(db, contract)

@router.get("/", response_model=List[ContractResponse])
async def list_contracts(
    db: AsyncSession = Depends(get_db),
    client_name: Optional[str] = Query(None, description="Фильтр по имени клиента"),
    status: Optional[str] = Query(None, description="Фильтр по статусу (active, closed, canceled)"),
    start_date: Optional[date] = Query(None, description="Дата начала диапазона"),
    end_date: Optional[date] = Query(None, description="Дата конца диапазона")
):
    """Получить список контрактов с фильтрацией"""
    return await get_contracts(db, client_name, status, start_date, end_date)

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract_detail(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить детали контракта"""
    contract = await get_contract(db, contract_id)
    if not contract:
        logger.warning(f"Contract {contract_id} not found")
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(contract_id: int, contract_data: ContractCreate, db: AsyncSession = Depends(get_db)):
    """Обновить контракт"""
    contract = await db.get(Contract, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    for key, value in contract_data.model_dump().items():
        if hasattr(contract, key):  # ✅ Безопасное обновление
            setattr(contract, key, value)

    await db.commit()
    await db.refresh(contract)
    return contract

@router.delete("/{contract_id}", status_code=204)
async def remove_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить контракт"""
    if not await delete_contract(db, contract_id):
        raise HTTPException(status_code=404, detail="Contract not found")
