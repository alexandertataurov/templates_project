"""
Template model definition.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Template(Base):
    """
    Template model for document generation.

    Attributes:
        template_type: Type of template (contract, invoice, etc.)
        display_name: User-friendly template name
        fields: JSON schema of template fields
        file_path: Path to template file
        user_id: Associated user identifier
    """

    __tablename__ = "templates"

    # Template details
    template_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="default"
    )
    display_name: Mapped[str] = mapped_column(
        String(255), nullable=False, default="Untitled"
    )
    fields: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    def __repr__(self):
        return f"<Template(id={self.id}, name={self.display_name})>"
