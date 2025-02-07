"""
Модель спецификаций.
"""

import logging
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Specification(Base):
    """Модель спецификации."""

    __tablename__ = "specifications"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)
    spec_number = Column(String(50), nullable=False, index=True)
    spec_date = Column(Date, nullable=False)

    contract = relationship("Contract", back_populates="specifications")


if settings.DEBUG:
    logger.debug("Модель Specification загружена")
