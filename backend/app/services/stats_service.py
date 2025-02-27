"""
Service for generating contract and payment statistics.
"""

from datetime import date, datetime
from typing import List, Dict, Any
from sqlalchemy import func, extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.addendum import Addendum
from app.models.payment import Payment
from app.models.invoice import Invoice


class StatsService:
    """Service for handling statistics operations."""

    @staticmethod
    async def get_total_contract_amount(db: AsyncSession) -> float:
        """Get total amount across all contracts."""
        result = await db.execute(select(func.sum(Contract.total_price)))
        return float(result.scalar() or 0)

    @staticmethod
    async def get_total_addendum_amount(db: AsyncSession) -> float:
        """Get total amount across all addendums."""
        result = await db.execute(select(func.sum(Addendum.additional_amount)))
        return float(result.scalar() or 0)

    @staticmethod
    async def get_monthly_stats(
        db: AsyncSession, year: int, month: int
    ) -> Dict[str, Any]:
        """
        Get monthly statistics.

        Args:
            db: Database session
            year: Year to get stats for
            month: Month to get stats for

        Returns:
            Dictionary with monthly statistics
        """
        # Get contracts created in the month
        contracts_query = select(func.count(Contract.id)).where(
            extract("year", Contract.contract_date) == year,
            extract("month", Contract.contract_date) == month,
        )

        # Get payments made in the month
        payments_query = select(func.sum(Payment.amount)).where(
            extract("year", Payment.payment_date) == year,
            extract("month", Payment.payment_date) == month,
        )

        # Get invoices issued in the month
        invoices_query = select(func.count(Invoice.id)).where(
            extract("year", Invoice.invoice_date) == year,
            extract("month", Invoice.invoice_date) == month,
        )

        # Execute queries
        contracts_result = await db.execute(contracts_query)
        payments_result = await db.execute(payments_query)
        invoices_result = await db.execute(invoices_query)

        return {
            "year": year,
            "month": month,
            "contracts_count": contracts_result.scalar() or 0,
            "total_payments": float(payments_result.scalar() or 0),
            "invoices_count": invoices_result.scalar() or 0,
        }


# Create service instance
stats_service = StatsService()


# Export individual functions for backward compatibility
async def get_monthly_stats(db: AsyncSession, year: int, month: int) -> Dict[str, Any]:
    """Get statistics for a specific month."""
    return await stats_service.get_monthly_stats(db, year, month)


async def get_total_contract_amount(db: AsyncSession) -> float:
    """Get total amount across all contracts."""
    return await stats_service.get_total_contract_amount(db)


async def get_total_addendum_amount(db: AsyncSession) -> float:
    """Get total amount across all addendums."""
    return await stats_service.get_total_addendum_amount(db)
