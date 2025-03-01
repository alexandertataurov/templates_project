"""
Journal model for audit logging.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class JournalEntry(Base):
    """
    Audit journal entry model.

    Attributes:
        event_type: Type of event (create, update, delete)
        user_id: User who performed the action
        document_id: ID of the document modified
        details: Additional event details
        ip_address: IP address of request
        timestamp: When the event occurred
    """

    __tablename__ = "journal_entries"

    # Event details
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"), index=True
    )
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # User info
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))  # IPv6 length

    # Metadata
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User")
    document: Mapped[Optional["Document"]] = relationship("Document")
