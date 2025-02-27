"""
Service for managing contract appendices.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.appendix import Appendix
from app.schemas.appendix import AppendixCreate, AppendixUpdate
from app.services.base_service import BaseService


class AppendixService(BaseService[Appendix, AppendixCreate, AppendixUpdate]):
    """Service for handling appendix operations."""

    async def get_by_contract(
        self, db: AsyncSession, contract_id: int, *, include_details: bool = False
    ) -> List[Appendix]:
        """
        Get all appendices for a specific contract.

        Args:
            db: Database session
            contract_id: Contract ID
            include_details: Whether to include related details

        Returns:
            List of appendices
        """
        query = select(Appendix).where(Appendix.contract_id == contract_id)

        if include_details:
            query = query.options(selectinload(Appendix.contract))

        result = await db.execute(query)
        return result.scalars().all()

    async def get_with_details(
        self, db: AsyncSession, appendix_id: int
    ) -> Optional[Appendix]:
        """Get appendix with all related details."""
        query = (
            select(Appendix)
            .options(selectinload(Appendix.contract))
            .filter(Appendix.id == appendix_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


# Create service instance
appendix_service = AppendixService(Appendix)


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
