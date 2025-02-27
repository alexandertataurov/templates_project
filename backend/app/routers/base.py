"""
Base router configuration and common dependencies.
"""

from typing import Annotated, Any, Tuple
from fastapi import Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Common dependencies
DbSession = Annotated[AsyncSession, Depends(get_db)]

# Common path parameters
ContractId = Annotated[
    int, Path(title="Contract ID", description="The ID of the contract", gt=0)
]

InvoiceId = Annotated[
    int, Path(title="Invoice ID", description="The ID of the invoice", gt=0)
]


# Common query parameters
def pagination_params(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)
) -> Tuple[int, int]:
    return skip, limit


PaginationParams = Annotated[Tuple[int, int], Depends(pagination_params)]


# Common response models
class SuccessResponse:
    """Standard success response."""

    def __init__(self, message: str, data: Any = None):
        self.success = True
        self.message = message
        if data is not None:
            self.data = data
