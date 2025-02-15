"""
Модель инвойсов.
"""

import logging
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Invoice(Base):
    """Модель инвойса."""

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(
        Integer,
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)

    contract = relationship("Contract", back_populates="invoices")
    payments = relationship(
        "Payment", back_populates="invoice", cascade="all, delete-orphan"
    )


if settings.DEBUG:
    logger.debug("Модель Invoice загружена")
