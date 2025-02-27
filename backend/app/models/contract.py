"""
Contract model definition.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .specification import Specification
    from .addendum import Addendum
    from .appendix import Appendix
    from .invoice import Invoice


class Contract(Base):
    """
    Contract model representing business agreements.

    Attributes:
        contract_number: Unique contract identifier
        contract_date: Date when contract was signed
        place_of_signing: Location where contract was signed
        valid_date: Contract expiration date
        supplier_details: Supplier information
        buyer_details: Buyer information
        goods_details: Product information
        related_documents: Associated documents
    """

    __tablename__ = "contracts"

    # Contract details
    contract_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    contract_date: Mapped[date] = mapped_column(Date, nullable=False)
    place_of_signing: Mapped[str] = mapped_column(String(255), nullable=False)
    valid_date: Mapped[Optional[date]] = mapped_column(Date)

    # Supplier details
    supplier_name: Mapped[str] = mapped_column(String(255), nullable=False)
    supplier_address: Mapped[str] = mapped_column(String(255), nullable=False)
    supplier_bank: Mapped[str] = mapped_column(String(255), nullable=False)
    supplier_account: Mapped[str] = mapped_column(String(50), nullable=False)

    # Buyer details
    buyer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    buyer_address: Mapped[str] = mapped_column(String(255), nullable=False)
    buyer_bank: Mapped[str] = mapped_column(String(255), nullable=False)
    buyer_account: Mapped[str] = mapped_column(String(50), nullable=False)

    # Goods details
    goods_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_per_unit: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Related documents
    specifications: Mapped[List["Specification"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
    addendums: Mapped[List["Addendum"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
    appendices: Mapped[List["Appendix"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
    invoices: Mapped[List["Invoice"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )
