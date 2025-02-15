from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.addendum import Addendum
from app.schemas.addendum import AddendumCreate


async def create_addendum(
    db: AsyncSession, contract_id: int, addendum_data: AddendumCreate
):
    addendum = Addendum(
        **addendum_data.dict(), contract_id=contract_id
    )  # ✅ Исправлено
    db.add(addendum)
    await db.commit()
    await db.refresh(addendum)
    return addendum


async def get_addendums(db: AsyncSession, contract_id: int):
    result = await db.execute(
        select(Addendum).where(Addendum.contract_id == contract_id)
    )
    return result.scalars().all()


async def get_addendum(db: AsyncSession, addendum_id: int):
    return await db.get(Addendum, addendum_id)


async def delete_addendum(db: AsyncSession, addendum_id: int):
    addendum = await get_addendum(db, addendum_id)
    if addendum:
        await db.delete(addendum)
        await db.commit()
        return True
    return False
