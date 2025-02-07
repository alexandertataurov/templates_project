"""
Модель контрактов.
"""

import logging
from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Contract(Base):
    """Модель контракта."""

    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, nullable=False, index=True)
    contract_date = Column(Date, nullable=False)
    place_of_signing = Column(String(255), nullable=False)
    valid_date = Column(Date, nullable=True)

    supplier_name = Column(String(255), nullable=False)
    supplier_address = Column(String(255), nullable=False)

    buyer_name = Column(String(255), nullable=False)
    buyer_address = Column(String(255), nullable=False)

    goods_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)

    specifications = relationship("Specification", back_populates="contract", cascade="all, delete-orphan")
    addendums = relationship("Addendum", back_populates="contract", cascade="all, delete-orphan")
    appendices = relationship("Appendix", back_populates="contract", cascade="all, delete-orphan", passive_deletes=True)
    invoices = relationship("Invoice", back_populates="contract", cascade="all, delete-orphan")


if settings.DEBUG:
    logger.debug("Модель Contract загружена")
