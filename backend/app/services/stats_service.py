from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.addendum import Addendum
from app.models.contract import Contract


async def get_total_contract_amount(db: AsyncSession):
    """Получает сумму всех контрактов"""
    result = await db.execute(select(func.sum(Contract.total_amount)))
    return result.scalar() or 0


async def get_total_addendum_amount(db: AsyncSession):
    """Получает сумму всех Доп. Соглашений"""
    result = await db.execute(select(func.sum(Addendum.additional_amount)))
    return result.scalar() or 0


async def get_monthly_stats(db: AsyncSession, year: int):
    """Получает статистику по суммам контрактов за каждый месяц указанного года"""
    result = await db.execute(
        select(
            func.extract("month", Contract.contract_date),
            func.sum(Contract.total_amount),
        )
        .where(func.extract("year", Contract.contract_date) == year)
        .group_by(func.extract("month", Contract.contract_date))
    )
    return [
        {"month": int(row[0]), "total_amount": float(row[1])} for row in result.all()
    ]
