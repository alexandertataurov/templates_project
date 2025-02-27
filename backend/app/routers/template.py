"""
Маршруты для управления шаблонами документов.
"""

import logging
from typing import List, Dict, Union, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.template_service import TemplateManager
from app.services.field_extractor import extract_dynamic_fields
from app.config import settings
from pathlib import Path
from app.models.template import Template
import json

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/templates",
    tags=["Templates"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Dict])
async def list_templates(db: AsyncSession = Depends(get_db)):
    """Возвращает список шаблонов."""
    try:
        return await TemplateManager.list_templates(db)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/upload")
async def upload_template(
    template_type: str = Form(...),
    display_name: str = Form(...),
    fields: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Загружает новый шаблон."""
    try:
        # Parse fields from JSON string
        try:
            parsed_fields = json.loads(fields)
            if not isinstance(parsed_fields, list):
                raise HTTPException(status_code=422, detail="Fields must be a list")
        except json.JSONDecodeError:
            raise HTTPException(status_code=422, detail="Invalid fields format")

        template = await TemplateManager.create_template(
            db,
            {
                "template_type": template_type,
                "display_name": display_name,
                "fields": parsed_fields,
                "file": file,
            },
        )

        return {"id": template.id, "message": "Template uploaded successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Upload failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
async def extract_fields_endpoint(file: UploadFile = File(...)):
    """Извлекает поля из загруженного файла."""
    try:
        logger.debug(
            "Received file for field extraction: %s (type: %s)",
            file.filename,
            
            file.content_type,
        )

        fields = await extract_dynamic_fields(file)
        logger.info("Successfully extracted %d fields", len(fields))
        return {"fields": fields}

    except FileNotFoundError as e:
        logger.error("File not found: %s - %s", file.filename, str(e))
        raise HTTPException(status_code=400, detail="File not found")
    except ValueError as e:
        logger.error("Invalid file format: %s - %s", file.filename, str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error extracting fields: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to extract fields: {str(e)}"
        )


@router.post("/update")
async def update_template(
    template_id: int = Form(...),
    display_name: Optional[str] = Form(None),
    fields: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    
    """Обновляет существующий шаблон."""
    try:
        logger.info("Received update request for template %d", template_id)

        # Get template
        template = await db.get(Template, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        # Update fields if provided
        if display_name is not None:
            template.display_name = display_name

        if fields is not None:
            try:
                template.fields = json.loads(fields)
            except json.JSONDecodeError as e:
                logger.error("Invalid JSON in fields: %s", str(e))
                raise HTTPException(status_code=422, detail="Invalid fields format")

        await db.commit()
        await db.refresh(template)

        return {
            "message": "Template updated successfully",
            "template": {
                "id": template.id,
                "display_name": template.display_name,
                "fields": template.fields,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Failed to update template: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{template_id}")
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет шаблон по ID."""
    try:
        logger.info("Attempting to delete template with ID: %d", template_id)

        # Check if template exists
        template = await db.get(Template, template_id)
        if not template:
            logger.error("Template not found: %d", template_id)
            raise HTTPException(
                status_code=404, detail=f"Template with ID {template_id} not found"
            )

        # Delete associated file if it exists
        if template.file_path:
            try:
                file_path = Path(template.file_path)
                if file_path.exists():
                    file_path.unlink()
                    logger.info("Deleted template file: %s", template.file_path)
            except Exception as e:
                logger.warning("Failed to delete template file: %s", str(e))

        # Delete template from database
        await db.delete(template)
        await db.commit()

        logger.info("Successfully deleted template: %d", template_id)
        return {"message": f"Template {template_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Error deleting template: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to delete template: {str(e)}"
        )
