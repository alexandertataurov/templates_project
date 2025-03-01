"""
Generic document model definition.
"""

from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    Date,
    JSON,
    ForeignKey,
    UniqueConstraint,
)  # Added ForeignKeyfrom sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship  # Added mapped_column
from app.core.database import Base

if TYPE_CHECKING:
    from .document import Document  # For self-referencing relationships


class Document(Base):
    """
    Generic document model for all types (e.g., contracts, specifications, invoices).

    Attributes:
        id: Unique identifier
        document_type: Type of document (e.g., "contract", "specification", "invoice")
        reference_number: Unique identifier for the document
        created_date: Date of creation
        dynamic_fields: JSON field for storing type-specific data
        parent_id: Optional reference to a parent document
    """

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    reference_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    created_date: Mapped[date] = mapped_column(Date, nullable=False)
    dynamic_fields: Mapped[dict] = mapped_column(JSON, nullable=True, default={})
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), nullable=True
    )

    # Self-referential relationship for parent/child documents
    children: Mapped[List["Document"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    parent: Mapped[Optional["Document"]] = relationship(
        back_populates="children", remote_side=[id]
    )

    __table_args__ = (
        UniqueConstraint("document_type", "reference_number", name="uq_doc_type_ref"),
    )
