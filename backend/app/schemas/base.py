"""
Base schema classes and common types.
"""

from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Annotated, TypeVar, Optional, List, Dict
from pydantic import BaseModel, Field, condecimal
from enum import Enum  # Import from enum module instead of typing

# Common type definitions
PriceType = Annotated[
    condecimal(max_digits=10, decimal_places=2),
    Field(description="Price field with 2 decimal places"),
]

DateType = Annotated[date, Field(description="Date in ISO format (YYYY-MM-DD)")]

# Generic type for ID fields
IdType = TypeVar("IdType", bound=int)


class BaseSchema(BaseModel):
    """Base schema with common configurations."""

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"example": {}},  # Override in subclasses
    }


class BaseResponseSchema(BaseSchema):
    """Base schema for response models."""

    id: int = Field(description="Unique identifier")
