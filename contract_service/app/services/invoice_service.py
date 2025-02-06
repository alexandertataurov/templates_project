from app.services.base_service import BaseService

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate

async def create_invoice(db: AsyncSession, contract_id: int, invoice_data: InvoiceCreate):
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
