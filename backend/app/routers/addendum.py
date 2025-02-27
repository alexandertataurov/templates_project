"""
Addendum management endpoints.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.addendum import AddendumCreate, AddendumResponse
from app.services import addendum_service
from app.config import settings
from .base import DbSession, ContractId

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts/{contract_id}/addendums", tags=["Addendums"])


@router.post(
    "/",
    response_model=AddendumResponse,
    summary="Create new addendum",
    description="Creates a new addendum for a specific contract",
)
async def create_addendum(
    contract_id: ContractId, addendum: AddendumCreate, db: DbSession
) -> AddendumResponse:
    """
    Create a new addendum.

    Args:
        contract_id: Contract ID
        addendum: Addendum data
        db: Database session

    Returns:
        Created addendum

    Raises:
        HTTPException: If creation fails
    """
    if settings.DEBUG:
        logger.debug(
            "Создание нового дополнительного соглашения для контракта %d", contract_id
        )
    return await addendum_service.create(db, contract_id, addendum)


@router.get(
    "/",
    response_model=List[AddendumResponse],
    summary="List addendums",
    description="Get all addendums for a specific contract",
)
async def list_addendums(
    contract_id: ContractId, db: DbSession
) -> List[AddendumResponse]:
    """Get list of addendums."""
    if settings.DEBUG:
        logger.debug(
            "Получение списка дополнительных соглашений для контракта %d", contract_id
        )
    return await addendum_service.get_multi(db, contract_id)


@router.delete(
    "/{addendum_id}",
    status_code=204,
    summary="Delete addendum",
    description="Delete an addendum from a contract",
)
async def delete_addendum(
    contract_id: ContractId, addendum_id: int, db: DbSession
) -> None:
    """Delete an addendum."""
    if settings.DEBUG:
        logger.debug(
            "Удаление дополнительного соглашения ID: %d из контракта %d",
            addendum_id,
            contract_id,
        )

    if not await addendum_service.delete(db, addendum_id):
        logger.warning("Дополнительное соглашение ID: %d не найдено", addendum_id)
        raise HTTPException(status_code=404, detail="Addendum not found")
