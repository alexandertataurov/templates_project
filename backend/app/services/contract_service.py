"""
Service for managing contracts.
"""

from datetime import date
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate
from app.services.base_service import BaseService


class ContractService(BaseService[Contract, ContractCreate, ContractUpdate]):
    """Service for handling contract operations."""

    async def get_by_filters(
        self,
        db: AsyncSession,
        *,
        client_name: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Contract]:
        """
        Get contracts with optional filters.

        Args:
            db: Database session
            client_name: Optional client name filter
            status: Optional status filter
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of contracts matching the filters
        """
        query = select(Contract)
        filters = []

        if client_name:
            filters.append(Contract.client_name.ilike(f"%{client_name}%"))
        if status:
            filters.append(Contract.status == status)
        if start_date and end_date:
            filters.append(
                and_(
                    Contract.contract_date >= start_date,
                    Contract.contract_date <= end_date,
                )
            )

        if filters:
            query = query.where(*filters)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_with_relations(
        self, db: AsyncSession, contract_id: int
    ) -> Optional[Contract]:
        """Get contract with all related entities."""
        query = (
            select(Contract)
            .options(
                selectinload(Contract.addendums),
                selectinload(Contract.appendices),
                selectinload(Contract.specifications),
                selectinload(Contract.invoices),
            )
            .filter(Contract.id == contract_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


# Create service instance
contract_service = ContractService(Contract)


# Export individual functions for backward compatibility
async def get_contract(db: AsyncSession, contract_id: int) -> Optional[Contract]:
    """Get a contract by ID."""
    return await contract_service.get(db, contract_id)


async def get_contracts(db: AsyncSession) -> List[Contract]:
    """Get all contracts."""
    return await contract_service.get_multi(db)
