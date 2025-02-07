"""
Модель платежей.
"""

import logging
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Payment(Base):
    """Модель платежа."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="payments")


if settings.DEBUG:
    logger.debug("Модель Payment загружена")
