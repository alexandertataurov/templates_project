from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.addendum_service import create_addendum, get_addendums, delete_addendum
from app.schemas.addendum import AddendumCreate, AddendumResponse
from typing import List

router = APIRouter(prefix="/contracts/{contract_id}/addendums", tags=["Addendums"])

@router.post("/", response_model=AddendumResponse)
async def create_new_addendum(contract_id: int, addendum: AddendumCreate, db: AsyncSession = Depends(get_db)):
    return await create_addendum(db, contract_id, addendum)

@router.get("/", response_model=List[AddendumResponse])
async def list_addendums(contract_id: int, db: AsyncSession = Depends(get_db)):
    return await get_addendums(db, contract_id)

@router.delete("/{addendum_id}", status_code=204)
async def remove_addendum(contract_id: int, addendum_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_addendum(db, addendum_id):
        raise HTTPException(status_code=404, detail="Addendum not found")
