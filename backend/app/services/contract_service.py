from datetime import date
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.contract import Contract
from app.schemas.contract import ContractCreate


async def create_contract(db: AsyncSession, contract_data: ContractCreate):
    contract = Contract(**contract_data.dict())  # ✅ Исправлено
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract


async def get_contracts(
    db: AsyncSession,
    client_name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Contract]:
    query = select(Contract)

    # Добавляем фильтры, если они указаны
    filters = []
    if client_name:
        filters.append(Contract.client_name.ilike(f"%{client_name}%"))
    if status:
        filters.append(Contract.status == status)
    if start_date and end_date:
        filters.append(
            and_(
                Contract.contract_date >= start_date, Contract.contract_date <= end_date
            )
        )

    if filters:
        query = query.where(*filters)

    result = await db.execute(query)
    return result.scalars().all()


async def get_contract(db: AsyncSession, contract_id: int):
    """Fetch contract by ID."""
    result = await db.execute(select(Contract).filter(Contract.id == contract_id))
    return result.scalars().first()


async def delete_contract(db: AsyncSession, contract_id: int):
    contract = await get_contract(db, contract_id)
    if contract:
        await db.delete(contract)
        await db.commit()
        return True
    return False
