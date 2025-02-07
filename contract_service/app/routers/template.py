"""
Маршруты для управления шаблонами документов.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.template_service import TemplateManager
from app.config import settings  # ✅ Добавляем Debug Mode

router = APIRouter(prefix="/templates", tags=["Templates"])

logger = logging.getLogger(__name__)


@router.get("/check-status")
async def check_status():
    """
    Проверяет, загружены ли шаблоны.

    :return: Статус.
    """
    try:
        status = await TemplateManager.check_status()
        if settings.DEBUG:
            logger.debug("Debug Mode: Checking template status...")
        logger.info("Check status result: %s", status)
        return status
    except Exception as e:
        logger.error("Error checking status: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при проверке статуса.")


@router.post("/start-setup")
async def start_setup():
    """
    Запускает процесс создания шаблонов.

    :return: Результат запуска.
    """
    try:
        if settings.DEBUG:
            logger.debug("Debug Mode: Starting template setup...")
        result = await TemplateManager.start_setup()
        logger.info("Setup started successfully.")
        return result
    except Exception as e:
        logger.error("Error starting setup: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при запуске настройки.")


@router.post("/define-fields")
async def define_fields(fields: List[str]):
    """
    Сохраняет динамические поля.

    :param fields: Список полей.
    :return: Подтверждение сохранения.
    """
    if settings.DEBUG:
        logger.debug("Debug Mode: Received fields: %s", fields)
    
    try:
        result = await TemplateManager.define_fields(fields)
        logger.info("Fields defined successfully: %s", result)
        return result
    except Exception as e:
        logger.error("Error defining fields: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при определении полей.")


@router.get("/instruction")
async def get_instruction():
    """
    Возвращает список динамических полей для формирования инструкции.

    :return: Данные инструкции.
    """
    try:
        instruction = await TemplateManager.get_instruction()
        if settings.DEBUG:
            logger.debug("Debug Mode: Instruction data fetched: %s", instruction)
        logger.info("Instruction data retrieved.")
        return instruction
    except Exception as e:
        logger.error("Error fetching instruction: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при получении инструкции.")


@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...),
    template_type: str = Form(...),
    display_name: str = Form(...),
    fields: List[str] = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Загружает шаблон и сохраняет его в БД с динамическими полями.

    :param file: Загружаемый файл.
    :param template_type: Тип шаблона.
    :param display_name: Название шаблона.
    :param fields: Динамические поля.
    :param db: Сессия базы данных.
    :return: Подтверждение загрузки.
    """
    if settings.DEBUG:
        logger.debug(
            "Debug Mode: Uploading file: %s, type: %s, name: %s, fields: %s",
            file.filename, template_type, display_name, fields
        )

    try:
        result = await TemplateManager.upload_template(
            file, template_type, display_name, fields, db
        )
        logger.info("✅ Template uploaded successfully: %s", result)
        return result
    except Exception as e:
        logger.error("❌ Upload Error: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при загрузке шаблона.")


@router.post("/update")
async def update_template(
    template_id: int = Form(...),
    display_name: str = Form(...),
    fields: List[str] = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Обновляет динамические поля и display_name для шаблона.

    :param template_id: ID шаблона.
    :param display_name: Новое имя шаблона.
    :param fields: Новый список полей.
    :param db: Сессия базы данных.
    :return: Подтверждение обновления.
    """
    if settings.DEBUG:
        logger.debug("Debug Mode: Updating template ID: %d", template_id)

    try:
        updated_data = {"display_name": display_name, "dynamic_fields": fields}
        result = await TemplateManager.update_template(template_id, updated_data, db)
        logger.info("Template updated successfully: %s", result)
        return result
    except Exception as e:
        logger.error("Error updating template %d: %s", template_id, e)
        raise HTTPException(status_code=500, detail="Ошибка при обновлении шаблона.")


@router.post("/delete")
async def delete_template(
    template_type: str = Form(...),
    display_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаляет шаблон по типу и названию.

    :param template_type: Тип шаблона.
    :param display_name: Название шаблона.
    :param db: Сессия базы данных.
    :return: Подтверждение удаления.
    """
    if settings.DEBUG:
        logger.debug("Debug Mode: Deleting template Type='%s', Name='%s'", template_type, display_name)

    try:
        result = await TemplateManager.delete_template(template_type, display_name, db)

        if not result:
            logger.warning("Template not found for deletion: Type='%s', Name='%s'", template_type, display_name)
            raise HTTPException(status_code=404, detail=f"Шаблон '{display_name}' не найден.")

        logger.info("Template deleted successfully: %s", result)
        return result
    except HTTPException as http_ex:
        logger.error("HTTP Exception: %s", http_ex.detail)
        raise http_ex
    except Exception as e:
        logger.exception("Unexpected error while deleting template: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении шаблона.")


@router.get("/")
async def list_templates(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список шаблонов с полной информацией из базы данных.

    :param db: Сессия базы данных.
    :return: Список шаблонов.
    """
    if settings.DEBUG:
        logger.debug("Debug Mode: Fetching template list...")

    try:
        templates = await TemplateManager.list_templates(db)
        logger.info("Fetched templates: %s", templates)
        return templates
    except Exception as e:
        logger.error("Error fetching templates: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при получении списка шаблонов.")
