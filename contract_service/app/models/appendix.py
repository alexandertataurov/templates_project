"""
Модель приложений (Appendices).
"""

import logging
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

logger = logging.getLogger(__name__)


class Appendix(Base):
    """Модель приложения."""

    __tablename__ = "appendices"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)
    appendix_number = Column(String(50), nullable=False, index=True)
    appendix_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    contract = relationship("Contract", back_populates="appendices")


if settings.DEBUG:
    logger.debug("Модель Appendix загружена")
