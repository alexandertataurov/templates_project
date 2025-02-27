"""
Service for managing invoice payments.
"""

from typing import List, Optional
from datetime import date
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.services.base_service import BaseService


class PaymentService(BaseService[Payment, PaymentCreate, PaymentUpdate]):
    """Service for handling payment operations."""

    async def get_by_invoice(
        self, db: AsyncSession, invoice_id: int, *, include_details: bool = False
    ) -> List[Payment]:
        """
        Get all payments for a specific invoice.

        Args:
            db: Database session
            invoice_id: Invoice ID
            include_details: Whether to include related details

        Returns:
            List of payments
        """
        query = select(Payment).where(Payment.invoice_id == invoice_id)

        if include_details:
            query = query.options(
                selectinload(Payment.invoice), selectinload(Payment.invoice.contract)
            )

        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_date_range(
        self, db: AsyncSession, start_date: date, end_date: date
    ) -> List[Payment]:
        """Get payments within a date range."""
        query = (
            select(Payment)
            .where(
                and_(
                    Payment.payment_date >= start_date, Payment.payment_date <= end_date
                )
            )
            .options(selectinload(Payment.invoice))
        )
        result = await db.execute(query)
        return result.scalars().all()


# Create service instance
payment_service = PaymentService(Payment)


async def create_payment(
    db: AsyncSession, invoice_id: int, payment_data: PaymentCreate
):
    payment = Payment(**payment_data.model_dump(), invoice_id=invoice_id)
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_payments(db: AsyncSession, invoice_id: int):
    result = await db.execute(select(Payment).where(Payment.invoice_id == invoice_id))
    return result.scalars().all()


async def get_payment(db: AsyncSession, payment_id: int):
    return await db.get(Payment, payment_id)


async def delete_payment(db: AsyncSession, payment_id: int):
    payment = await get_payment(db, payment_id)
    if payment:
        await db.delete(payment)
        await db.commit()
        return True
    return False
