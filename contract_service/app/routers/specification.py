from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.specification_service import create_specification, get_specifications, delete_specification
from app.schemas.specification import SpecificationCreate, SpecificationResponse
from typing import List
from app.services.specification_service import get_contract_by_specification
from sqlalchemy.orm import Session


router = APIRouter(prefix="/contracts/{contract_id}/specifications", tags=["Specifications"])

@router.post("/", response_model=SpecificationResponse)
async def create_new_specification(contract_id: int, specification: SpecificationCreate, db: AsyncSession = Depends(get_db)):
    return await create_specification(db, contract_id, specification)

@router.get("/contract/{specification_id}")  # Убедись, что параметр передается в URL
async def get_contract_by_specification_endpoint(
    specification_id: int, db: Session = Depends(get_db)
):
    contract = await get_contract_by_specification(db, specification_id)
    return contract

@router.delete("/{spec_id}", status_code=204)
async def remove_specification(contract_id: int, spec_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить спецификацию"""
    contract = await get_contract_by_specification(db, specification_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if not await delete_specification(db, spec_id):
        raise HTTPException(status_code=404, detail="Specification not found")
