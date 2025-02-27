"""
Payment model definition.
"""

from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .invoice import Invoice


class Payment(Base):
    """
    Payment model representing invoice payments.

    Attributes:
        invoice_id: Associated invoice identifier
        payment_date: Date of payment
        amount: Payment amount
        invoice: Associated invoice
    """

    __tablename__ = "payments"

    # Relationship fields
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Payment details
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    reference: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relationships
    invoice: Mapped["Invoice"] = relationship(back_populates="payments")
