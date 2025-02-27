"""
Service for managing contract addendums.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.addendum import Addendum
from app.schemas.addendum import AddendumCreate, AddendumUpdate
from app.services.base_service import BaseService


class AddendumService(BaseService[Addendum, AddendumCreate, AddendumUpdate]):
    """Service for handling addendum operations."""

    async def get_by_contract(
        self, db: AsyncSession, contract_id: int, *, include_details: bool = False
    ) -> List[Addendum]:
        """
        Get all addendums for a specific contract.

        Args:
            db: Database session
            contract_id: Contract ID
            include_details: Whether to include related details

        Returns:
            List of addendums
        """
        query = select(Addendum).where(Addendum.contract_id == contract_id)

        if include_details:
            query = query.options(
                selectinload(Addendum.contract), selectinload(Addendum.payments)
            )

        result = await db.execute(query)
        return result.scalars().all()

    async def get_with_details(
        self, db: AsyncSession, addendum_id: int
    ) -> Optional[Addendum]:
        """Get addendum with all related details."""
        query = (
            select(Addendum)
            .options(selectinload(Addendum.contract), selectinload(Addendum.payments))
            .filter(Addendum.id == addendum_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


# Create service instance
addendum_service = AddendumService(Addendum)


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
