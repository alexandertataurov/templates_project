from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contract import Contract
from app.models.addendum import Addendum

async def update_contract_exchange_rate(db: AsyncSession, contract_id: int, new_rate: float):
    contract = await db.get(Contract, contract_id)
    if contract:
        contract.exchange_rate = new_rate
        await db.commit()
        await db.refresh(contract)
        return contract
    return None

async def update_addendum_exchange_rate(db: AsyncSession, addendum_id: int, new_rate: float):
    addendum = await db.get(Addendum, addendum_id)
    if addendum:
        addendum.exchange_rate = new_rate
        await db.commit()
        await db.refresh(addendum)
        return addendum
    return None
