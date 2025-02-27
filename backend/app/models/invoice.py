"""
Invoice model definition.
"""

from datetime import date
from decimal import Decimal
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .contract import Contract
    from .payment import Payment


class Invoice(Base):
    """
    Invoice model representing payment requests.

    Attributes:
        contract_id: Associated contract identifier
        invoice_number: Unique invoice identifier
        invoice_date: Date of issue
        due_date: Payment due date
        total_amount: Total invoice amount
        payments: Associated payments
    """

    __tablename__ = "invoices"

    # Relationship fields
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Invoice details
    invoice_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Relationships
    contract: Mapped["Contract"] = relationship(back_populates="invoices")
    payments: Mapped[List["Payment"]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan"
    )
