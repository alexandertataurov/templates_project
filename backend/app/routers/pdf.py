"""
Маршруты для экспорта документов (PDF, DOCX).
"""

import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.contract import ContractBase
from app.services.contract_service import get_contract
from app.services.pdf_service import convert_docx_to_pdf, generate_contract_docx
from app.config import settings  # ✅ Добавлен Debug Mode

logger = logging.getLogger(__name__)

TEMPLATE_DIR = "templates/"

router = APIRouter(prefix="/pdf", tags=["PDF Export"])


@router.get("/contract/{contract_id}", response_class=FileResponse)
async def export_contract(
    contract_id: int,
    format: str = Query("pdf", enum=["pdf", "docx"], description="Output file format"),
    template: str = Query("contract_template.docx", description="Template file to use"),
    exclude_fields: list[str] = Query([], description="List of fields to exclude"),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """
    Генерация контракта в формате PDF или DOCX.
    """
    if settings.DEBUG:
        logger.debug("Генерация контракта %d в формате %s", contract_id, format)

    template_path = os.path.join(TEMPLATE_DIR, template)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=400, detail=f"Template {template} not found")

    contract = await get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_data = ContractBase.model_validate(contract.__dict__)
    contract_dict = contract_data.model_dump()

    for field in exclude_fields:
        contract_dict.pop(field, None)

    docx_path = await generate_contract_docx(ContractBase(**contract_dict), template)

    if format == "pdf":
        pdf_path = await convert_docx_to_pdf(docx_path)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"contract_{contract_id}.pdf",
        )

    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"contract_{contract_id}.docx",
    )
