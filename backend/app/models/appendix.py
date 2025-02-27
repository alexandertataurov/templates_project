"""
Appendix model definition.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .contract import Contract

from datetime import date
from typing import Optional
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Appendix(Base):
    """
    Appendix model representing contract attachments.

    Attributes:
        contract_id: Associated contract identifier
        appendix_number: Unique appendix identifier
        appendix_date: Date of attachment
        description: Appendix description
    """

    __tablename__ = "appendices"

    # Relationship fields
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE"), index=True, nullable=False
    )

    # Appendix details
    appendix_number: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    appendix_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    contract: Mapped["Contract"] = relationship(back_populates="appendices")
