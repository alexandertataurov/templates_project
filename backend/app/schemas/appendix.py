"""
Schema definitions for contract appendices.
"""

from typing import Optional
from pydantic import Field
from .common import DateType, BaseSchema, BaseResponseSchema


class AppendixBase(BaseSchema):
    """Base schema for appendix data."""

    appendix_number: str = Field(
        ..., max_length=50, description="Unique appendix number"
    )
    appendix_date: DateType
    description: Optional[str] = Field(
        None, max_length=1000, description="Appendix description"
    )
    document_type: str = Field(
        ..., max_length=50, description="Type of appendix document"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "appendix_number": "APP-2024-001",
                "appendix_date": "2024-01-15",
                "description": "Technical specifications",
                "document_type": "specifications",
            }
        }
    }


class AppendixCreate(AppendixBase):
    """Schema for creating a new appendix."""

    contract_id: int = Field(..., description="Associated contract ID")


class AppendixUpdate(AppendixBase):
    """Schema for updating appendix."""

    pass


class AppendixResponse(AppendixBase, BaseResponseSchema):
    """Schema for appendix response including ID and relationships."""

    contract_id: int = Field(..., description="Associated contract ID")
