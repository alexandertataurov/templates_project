"""
Service for managing exchange rates in contracts and addendums.
"""

from typing import Optional, Tuple, List
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.contract import Contract
from app.models.addendum import Addendum
from app.services.base_service import BaseService


class ExchangeRateService:
    """Service for handling exchange rate operations."""

    @staticmethod
    async def update_contract_rate(
        db: AsyncSession, contract_id: int, new_rate: Decimal
    ) -> Contract:
        """
        Update exchange rate for a contract.

        Args:
            db: Database session
            contract_id: Contract ID
            new_rate: New exchange rate

        Returns:
            Updated contract
        """
        contract = await db.get(Contract, contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        try:
            contract.exchange_rate = new_rate
            await db.commit()
            await db.refresh(contract)
            return contract
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update exchange rate: {str(e)}"
            )

    @staticmethod
    async def update_addendum_rate(
        db: AsyncSession, addendum_id: int, new_rate: Decimal
    ) -> Addendum:
        """Update exchange rate for an addendum."""
        addendum = await db.get(Addendum, addendum_id)
        if not addendum:
            raise HTTPException(status_code=404, detail="Addendum not found")

        try:
            addendum.exchange_rate = new_rate
            await db.commit()
            await db.refresh(addendum)
            return addendum
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update exchange rate: {str(e)}"
            )

    @staticmethod
    async def get_rates(
        db: AsyncSession, contract_id: int
    ) -> Tuple[Optional[Decimal], List[Decimal]]:
        """Get exchange rates for contract and its addendums."""
        contract = await db.get(Contract, contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        result = await db.execute(
            select(Addendum.exchange_rate).where(Addendum.contract_id == contract_id)
        )
        addendum_rates = [rate for (rate,) in result if rate is not None]

        return contract.exchange_rate, addendum_rates


# Create service instance
exchange_rate_service = ExchangeRateService()
