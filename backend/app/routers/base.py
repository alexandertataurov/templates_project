"""
Base router configuration and common dependencies.
"""

from typing import Annotated, Tuple, Any
from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_sync  # Updated to use sync version

# Common dependencies
DbSession = Annotated[AsyncSession, Depends(get_db_sync)]


# Common query parameters
def pagination_params(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items"),
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
