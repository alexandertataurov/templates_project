from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.appendix import Appendix
from app.schemas.appendix import AppendixCreate


async def create_appendix(
    db: AsyncSession, contract_id: int, appendix_data: AppendixCreate
):
    appendix = Appendix(**appendix_data.model_dump(), contract_id=contract_id)
    db.add(appendix)
    await db.commit()
    await db.refresh(appendix)
    return appendix


async def get_appendices(db: AsyncSession, contract_id: int):
    result = await db.execute(
        select(Appendix).where(Appendix.contract_id == contract_id)
    )
    return result.scalars().all()


async def get_appendix(db: AsyncSession, appendix_id: int):
    return await db.get(Appendix, appendix_id)


async def delete_appendix(db: AsyncSession, appendix_id: int):
    appendix = await get_appendix(db, appendix_id)
    if appendix:
        await db.delete(appendix)
        await db.commit()
        return True
    return False
