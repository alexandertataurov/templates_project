"""
Service for managing contract invoices.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.services.base_service import BaseService


class InvoiceService(BaseService[Invoice, InvoiceCreate, InvoiceUpdate]):
    """Service for handling invoice operations."""

    async def get_by_contract(
        self, db: AsyncSession, contract_id: int, *, include_payments: bool = False
    ) -> List[Invoice]:
        """
        Get all invoices for a specific contract.

        Args:
            db: Database session
            contract_id: Contract ID
            include_payments: Whether to include payment details

        Returns:
            List of invoices
        """
        query = select(Invoice).where(Invoice.contract_id == contract_id)

        if include_payments:
            query = query.options(
                selectinload(Invoice.payments), selectinload(Invoice.contract)
            )

        result = await db.execute(query)
        return result.scalars().all()

    async def get_with_payments(
        self, db: AsyncSession, invoice_id: int
    ) -> Optional[Invoice]:
        """Get invoice with payment details."""
        query = (
            select(Invoice)
            .options(selectinload(Invoice.payments), selectinload(Invoice.contract))
            .filter(Invoice.id == invoice_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_unpaid(
        self, db: AsyncSession, contract_id: Optional[int] = None
    ) -> List[Invoice]:
        """Get unpaid invoices."""
        query = select(Invoice).where(Invoice.paid == False)  # noqa: E712

        if contract_id:
            query = query.where(Invoice.contract_id == contract_id)

        result = await db.execute(query)
        return result.scalars().all()


# Create service instance
invoice_service = InvoiceService(Invoice)


async def create_invoice(
    db: AsyncSession, contract_id: int, invoice_data: InvoiceCreate
):
    invoice = Invoice(**invoice_data.model_dump(), contract_id=contract_id)
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def get_invoices(db: AsyncSession, contract_id: int):
    result = await db.execute(select(Invoice).where(Invoice.contract_id == contract_id))
    return result.scalars().all()


async def get_invoice(db: AsyncSession, invoice_id: int):
    return await db.get(Invoice, invoice_id)


async def delete_invoice(db: AsyncSession, invoice_id: int):
    invoice = await get_invoice(db, invoice_id)
    if invoice:
        await db.delete(invoice)
        await db.commit()
        return True
    return False
