"""
Модель дополнительного соглашения (Addendum).
"""

import logging
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Addendum(Base):
    """Модель дополнительного соглашения."""

    __tablename__ = "addendums"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(
        Integer,
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    addendum_number = Column(String(50), nullable=False, index=True)
    addendum_date = Column(Date, nullable=False)
    invoice_number = Column(String(50), nullable=True, index=True)
    invoice_amount = Column(Numeric(15, 2), nullable=True)
    description = Column(String(255), nullable=True)

    contract = relationship("Contract", back_populates="addendums")


if settings.DEBUG:
    logger.debug("Модель Addendum загружена")
