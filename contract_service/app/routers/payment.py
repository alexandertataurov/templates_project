from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.payment_service import create_payment, get_payments
from app.schemas.payment import PaymentCreate, PaymentResponse
from typing import List

router = APIRouter(prefix="/invoices/{invoice_id}/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
async def create_new_payment(invoice_id: int, payment: PaymentCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый платеж для инвойса"""
    return await create_payment(db, invoice_id, payment)

@router.get("/", response_model=List[PaymentResponse])
async def list_payments(invoice_id: int, db: AsyncSession = Depends(get_db)):
    """Получить список платежей для инвойса"""
    return await get_payments(db, invoice_id)
