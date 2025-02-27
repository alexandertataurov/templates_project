"""
Contract management endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.contract import ContractCreate, ContractResponse
from app.services import contract_service
from .base import DbSession, ContractId, PaginationParams

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post(
    "/",
    response_model=ContractResponse,
    summary="Create new contract",
    description="Creates a new contract with the provided details",
)
async def create_contract(contract: ContractCreate, db: DbSession) -> ContractResponse:
    """
    Create a new contract.

    Args:
        contract: Contract data
        db: Database session

    Returns:
        Created contract

    Raises:
        HTTPException: If contract creation fails
    """
    try:
        return await contract_service.create(db, contract)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{contract_id}",
    response_model=ContractResponse,
    summary="Get contract details",
    description="Retrieves details of a specific contract",
)
async def get_contract(
    contract_id: ContractId,
    db: DbSession,
    include_related: bool = Query(
        False,
        description="Include related entities like addendums, specifications etc.",
    ),
) -> ContractResponse:
    """
    Get contract details.

    Args:
        contract_id: Contract ID
        db: Database session
        include_related: Whether to include related entities

    Returns:
        Contract details

    Raises:
        HTTPException: If contract not found
    """
    contract = await contract_service.get(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.get(
    "/",
    response_model=List[ContractResponse],
    summary="List contracts",
    description="Get a list of contracts with optional filtering",
)
async def list_contracts(
    db: DbSession,
    skip: int = Query(0, ge=0, description="Number of contracts to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of contracts to return"
    ),
    status: Optional[str] = Query(None, description="Filter by contract status"),
    client_name: Optional[str] = Query(None, description="Filter by client name"),
) -> List[ContractResponse]:
    """
    List contracts with pagination and filtering.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        client_name: Optional client name filter

    Returns:
        List of contracts
    """
    filters = {}
    if status:
        filters["status"] = status
    if client_name:
        filters["client_name"] = client_name

    return await contract_service.get_multi(db, skip=skip, limit=limit, filters=filters)
