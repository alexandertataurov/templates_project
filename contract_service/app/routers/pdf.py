from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.pdf_service import generate_contract_docx, convert_docx_to_pdf
from app.services.contract_service import get_contract
from app.schemas.contract import ContractBase
import os

TEMPLATE_DIR = "templates/"

router = APIRouter(prefix="/pdf", tags=["PDF Export"])

@router.get("/contract/{contract_id}", response_class=FileResponse, summary="Generate contract in DOCX or PDF")
async def export_contract(
    contract_id: int,
    format: str = Query(
        "pdf", enum=["pdf", "docx"], description="Output file format"
    ),
    template: str = Query(
        "contract_template.docx", description="Template file to use for contract generation"
    ),
    exclude_fields: list[str] = Query(
        [], description="List of fields to exclude from the contract"
    ),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Generates a contract document based on a selected template and optional field exclusions."""
    
    # Проверяем, существует ли шаблон
    template_path = os.path.join(TEMPLATE_DIR, template)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=400, detail=f"Template {template} not found")

    contract = await get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Конвертируем SQLAlchemy объект в Pydantic
    contract_data = ContractBase.model_validate(contract.__dict__)

    # Удаляем ненужные поля
    contract_dict = contract_data.model_dump()
    for field in exclude_fields:
        contract_dict.pop(field, None)

    # Генерируем DOCX
    docx_path = await generate_contract_docx(ContractBase(**contract_dict), template)

    # Конвертируем в PDF, если нужно
    if format == "pdf":
        pdf_path = await convert_docx_to_pdf(docx_path)
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"contract_{contract_id}.pdf")

    return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=f"contract_{contract_id}.docx")

@router.get("/templates", summary="List available contract templates")
async def list_templates():
    """Returns a list of available contract templates."""
    templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".docx")]
    return {"templates": templates}
