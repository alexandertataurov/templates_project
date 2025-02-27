"""
User model definition.
"""

from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    """
    User model for authentication and authorization.

    Attributes:
        username: Unique username
        email: User's email address
        full_name: User's full name
        is_active: Whether user account is active
        hashed_password: Encrypted password
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
