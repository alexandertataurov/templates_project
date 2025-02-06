from app.services.base_service import BaseServiceService

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

async def create_payment(db: AsyncSession, invoice_id: int, payment_data: PaymentCreate):
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
