"""
Addendum model definition.
"""

from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .contract import Contract


class Addendum(Base):
    """
    Addendum model representing contract amendments.

    Attributes:
        contract_id: Associated contract identifier
        addendum_number: Unique addendum identifier
        addendum_date: Date of amendment
        invoice_details: Related invoice information
        description: Amendment description
    """

    __tablename__ = "addendums"

    # Relationship fields
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Addendum details
    addendum_number: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    addendum_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Invoice details
    invoice_number: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    invoice_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    contract: Mapped["Contract"] = relationship(back_populates="addendums")
