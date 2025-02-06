from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.stats_service import get_total_contract_amount, get_total_addendum_amount, get_monthly_stats

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/total-contracts")
async def total_contracts(db: AsyncSession = Depends(get_db)):
    return {"total_contract_amount": await get_total_contract_amount(db)}

@router.get("/total-addendums")
async def total_addendums(db: AsyncSession = Depends(get_db)):
    return {"total_addendum_amount": await get_total_addendum_amount(db)}

@router.get("/monthly")
async def monthly_statistics(year: int = Query(..., description="Year for statistics"), db: AsyncSession = Depends(get_db)):
    return await get_monthly_stats(db, year)
