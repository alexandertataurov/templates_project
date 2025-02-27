"""
Schema definitions for the application.
"""

from .base import BaseSchema, BaseResponseSchema, PriceType, DateType
from .common import CurrencyEnum, StatusEnum
from .contract import ContractBase, ContractCreate, ContractResponse, ContractUpdate
from .addendum import AddendumBase, AddendumCreate, AddendumResponse, AddendumUpdate
from .appendix import AppendixBase, AppendixCreate, AppendixResponse, AppendixUpdate
from .invoice import InvoiceBase, InvoiceCreate, InvoiceResponse, InvoiceUpdate
from .payment import PaymentBase, PaymentCreate, PaymentResponse, PaymentUpdate
from .specification import (
    SpecificationBase,
    SpecificationCreate,
    SpecificationResponse,
    SpecificationUpdate,
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "BaseResponseSchema",
    "PriceType",
    "DateType",
    # Common types
    "CurrencyEnum",
    "StatusEnum",
    # Contract schemas
    "ContractBase",
    "ContractCreate",
    "ContractResponse",
    "ContractUpdate",
    # Addendum schemas
    "AddendumBase",
    "AddendumCreate",
    "AddendumResponse",
    "AddendumUpdate",
    # Appendix schemas
    "AppendixBase",
    "AppendixCreate",
    "AppendixResponse",
    "AppendixUpdate",
    # Invoice schemas
    "InvoiceBase",
    "InvoiceCreate",
    "InvoiceResponse",
    "InvoiceUpdate",
    # Payment schemas
    "PaymentBase",
    "PaymentCreate",
    "PaymentResponse",
    "PaymentUpdate",
    # Specification schemas
    "SpecificationBase",
    "SpecificationCreate",
    "SpecificationResponse",
    "SpecificationUpdate",
]
