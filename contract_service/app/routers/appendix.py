from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.appendix_service import create_appendix, get_appendices, delete_appendix
from app.schemas.appendix import AppendixCreate, AppendixResponse
from typing import List

router = APIRouter(prefix="/contracts/{contract_id}/appendices", tags=["Appendices"])

@router.post("/", response_model=AppendixResponse)
async def create_new_appendix(contract_id: int, appendix: AppendixCreate, db: AsyncSession = Depends(get_db)):
    return await create_appendix(db, contract_id, appendix)

@router.get("/", response_model=List[AppendixResponse])
async def list_appendices(contract_id: int, db: AsyncSession = Depends(get_db)):
    return await get_appendices(db, contract_id)

@router.delete("/{appendix_id}", status_code=204)
async def remove_appendix(contract_id: int, appendix_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_appendix(db, appendix_id):
        raise HTTPException(status_code=404, detail="Appendix not found")
