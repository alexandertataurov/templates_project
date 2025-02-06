from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.template_service import TemplateManager
from app.database import get_db

router = APIRouter(prefix="/templates", tags=["Templates"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/check-status")
async def check_status():
    """Проверяет, загружены ли шаблоны."""
    try:
        status = await TemplateManager.check_status()
        logger.info(f"Check status result: {status}")
        return status
    except Exception as e:
        logger.error(f"Error checking status: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при проверке статуса.")

@router.post("/start-setup")
async def start_setup():
    """Запускает процесс создания шаблонов."""
    try:
        result = await TemplateManager.start_setup()
        logger.info("Setup started successfully.")
        return result
    except Exception as e:
        logger.error(f"Error starting setup: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при запуске настройки.")

@router.post("/define-fields")
async def define_fields(fields: List[str]):
    """Сохраняет динамические поля."""
    logger.info(f"Received fields: {fields}")
    try:
        result = await TemplateManager.define_fields(fields)
        logger.info(f"Fields defined successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error defining fields: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при определении полей.")

@router.get("/instruction")
async def get_instruction():
    """
    Возвращает список динамических полей для формирования инструкции.
    Окончательное форматирование поручается фронтенду.
    """
    try:
        instruction = await TemplateManager.get_instruction()
        logger.info(f"Instruction data: {instruction}")
        return instruction
    except Exception as e:
        logger.error(f"Error fetching instruction: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении инструкции.")

@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...),
    template_type: str = Form(...),
    display_name: str = Form(...),
    fields: List[str] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Загружает шаблон и сохраняет его в БД с динамическими полями."""
    logger.info(f"📤 [UPLOAD] Получен файл: {file.filename}, type: {template_type}, name: {display_name}")
    logger.info(f"🔍 [UPLOAD] Полученные fields: {fields} ({type(fields)})")

    try:
        result = await TemplateManager.upload_template(file, template_type, display_name, fields, db)
        logger.info(f"✅ [UPLOAD] Шаблон загружен успешно: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [UPLOAD ERROR] Ошибка загрузки шаблона: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при загрузке шаблона.")


@router.post("/update")
async def update_template(
    template_id: int = Form(...),
    display_name: str = Form(...),
    fields: List[str] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновляет динамические поля и display_name для шаблона.
    """
    logger.info(f"Updating template ID: {template_id}, new name: {display_name}, fields: {fields}")
    try:
        updated_data = {
            "display_name": display_name,
            "dynamic_fields": fields
        }
        result = await TemplateManager.update_template(template_id, updated_data, db)
        logger.info(f"Template updated successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error updating template {template_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при обновлении шаблона.")

@router.post("/delete")
async def delete_template(
    template_type: str = Form(...),
    display_name: str = Form(...),
    db: AsyncSession = Depends(get_db)  # ✅ Добавляем передачу db
):
    """Удаляет шаблон по типу и названию."""
    logger.info(f"Received request to delete template. Type: {template_type}, Name: {display_name}")

    try:
        result = await TemplateManager.delete_template(template_type, display_name, db)
        
        if not result:
            logger.warning(f"Template not found for deletion: Type='{template_type}', Name='{display_name}'")
            raise HTTPException(status_code=404, detail=f"Шаблон '{display_name}' не найден.")

        logger.info(f"Template deleted successfully: {result}")
        return result

    except HTTPException as http_ex:
        logger.error(f"HTTP Exception: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logger.exception(f"Unexpected error while deleting template: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при удалении шаблона.")


@router.get("/")
async def list_templates(db: AsyncSession = Depends(get_db)):
    """Возвращает список шаблонов с полной информацией, полученной из базы данных."""
    try:
        templates = await TemplateManager.list_templates(db)
        logger.info(f"Fetched templates: {templates}")
        return templates
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении списка шаблонов.")
