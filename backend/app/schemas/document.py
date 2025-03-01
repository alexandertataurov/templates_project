"""
Document schema definitions.
"""

from typing import Optional, Dict, Any
from pydantic import Field
from .common import DateType, BaseSchema, BaseResponseSchema


class DocumentBase(BaseSchema):
    """Base schema for document data."""

    document_type: str = Field(
        ...,
        max_length=50,
        description="Type of document (e.g., contract, addendum, specification)",
    )
    reference_number: str = Field(
        ..., max_length=50, description="Unique reference number"
    )
    created_date: DateType
    dynamic_fields: Dict[str, Any] = Field(
        default={},
        description="Type-specific dynamic fields (e.g., supplier_name, total_price, notes)",
    )
    parent_id: Optional[int] = Field(
        None, description="ID of parent document, if applicable"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "document_type": "contract",
                "reference_number": "CNT-2025-001",
                "created_date": "2025-03-01",
                "dynamic_fields": {
                    "supplier_name": "Supplier Inc.",
                    "buyer_name": "Buyer Corp.",
                    "total_price": 1050.00,
                    "currency": "USD",
                },
                "parent_id": None,
            }
        }
    }


class DocumentCreate(DocumentBase):
    """Schema for creating a new document."""

    pass


class DocumentUpdate(DocumentBase):
    """Schema for updating a document."""

    document_type: Optional[str] = Field(None, max_length=50)
    reference_number: Optional[str] = Field(None, max_length=50)
    created_date: Optional[DateType] = None
    dynamic_fields: Optional[Dict[str, Any]] = Field(
        None, description="Updated dynamic fields"
    )
    parent_id: Optional[int] = Field(
        None, description="ID of parent document, if applicable"
    )


class DocumentResponse(DocumentBase, BaseResponseSchema):
    """Schema for document response including ID."""

    pass
