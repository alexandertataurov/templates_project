"""
Exchange rate management endpoints.
"""

from decimal import Decimal
from fastapi import APIRouter, HTTPException
from app.services import exchange_rate_service
from .base import DbSession, ContractId

router = APIRouter(prefix="/exchange-rate", tags=["Exchange Rates"])


@router.put(
    "/contract/{contract_id}",
    summary="Update contract exchange rate",
    description="Update the exchange rate for a specific contract",
)
async def update_contract_rate(
    contract_id: ContractId, new_rate: Decimal, db: DbSession
) -> dict:
    """
    Update contract exchange rate.

    Args:
        contract_id: Contract ID
        new_rate: New exchange rate value
        db: Database session

    Returns:
        Updated exchange rate info

    Raises:
        HTTPException: If rate is invalid or contract not found
    """
    if new_rate <= 0:
        raise HTTPException(status_code=400, detail="Exchange rate must be positive")

    contract = await exchange_rate_service.update_contract_rate(
        db, contract_id, new_rate
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return {"contract_id": contract_id, "new_exchange_rate": new_rate}
