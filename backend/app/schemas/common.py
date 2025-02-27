"""
Common schema types and utilities.
"""

from enum import Enum
from .base import PriceType, DateType, BaseSchema, BaseResponseSchema


class CurrencyEnum(str, Enum):
    """Supported currencies."""

    CNY = "CNY"
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class StatusEnum(str, Enum):
    """Common status values."""

    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DRAFT = "draft"


__all__ = [
    "PriceType",
    "DateType",
    "BaseSchema",
    "BaseResponseSchema",
    "CurrencyEnum",
    "StatusEnum",
    "IdType",
]
