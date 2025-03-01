"""
Маршруты для экспорта документов (PDF, DOCX).
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.document import DocumentBase
from app.services.document_service import document_service
from app.services.pdf_service import generate_document_docx, convert_docx_to_pdf
from app.core.config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pdf", tags=["PDF Export"])


@router.get("/{document_id}", response_class=FileResponse)
async def export_document(
    document_id: int,
    format: str = Query("pdf", enum=["pdf", "docx"], description="Output file format"),
    template: str = Query("default_template.docx", description="Template file to use"),
    exclude_fields: list[str] = Query([], description="List of fields to exclude"),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """
    Генерация документа в формате PDF или DOCX.
    """
    if Settings.DEBUG:
        logger.debug(
            "Генерация документа %d в формате %s с шаблоном %s",
            document_id,
            format,
            template,
        )

    document = await document_service.get(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document_data = DocumentBase(
        document_type=document.document_type,
        reference_number=document.reference_number,
        created_date=document.created_date,
        dynamic_fields=document.dynamic_fields,
        parent_id=document.parent_id,
    )
    document_dict = document_data.model_dump()
    for field in exclude_fields:
        document_dict["dynamic_fields"].pop(field, None)

    docx_path = await generate_document_docx(document_data, template)
    if format == "pdf":
        pdf_path = await convert_docx_to_pdf(docx_path)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{document.document_type}_{document_id}.pdf",
        )
    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{document.document_type}_{document_id}.docx",
    )
