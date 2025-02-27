"""
Сервис для управления шаблонами документов.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import uuid4

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.models.template import Template
from app.services.field_extractor import extract_dynamic_fields

# === Конфигурация путей ===
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
GENERATED_DIR = BASE_DIR / "assets" / "generated_docs"
FIELDS_FILE = TEMPLATES_DIR / "fields.json"
PRESETS_FILE = BASE_DIR / "assets" / "presets.json"

# Разрешённые типы шаблонов
REQUIRED_TEMPLATES = {"contract", "specification", "addendum"}

# Стандартный набор динамических полей
DEFAULT_DYNAMIC_FIELDS: Dict[str, List[str]] = {
    "contract": ["date", "buyer", "seller"],
    "specification": ["date", "product_list", "total_amount"],
    "addendum": ["date", "notes"],
}

# Стандартные пользовательские названия
DEFAULT_DISPLAY_NAMES: Dict[str, str] = {
    "contract": "Стандартный договор",
    "specification": "Стандартная спецификация",
    "addendum": "Стандартное дополнение",
}

# Создание директорий
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# Настройка логирования
logger = logging.getLogger(__name__)


class TemplateManager:
    """Сервис для работы с шаблонами, пресетами и их инициализацией в БД."""

    UPLOAD_DIR = "app/assets/templates"

    @staticmethod
    async def read_json(file_path: Path, default: Optional[Dict] = None) -> Dict:
        """Асинхронно читает JSON-файл."""
        if not file_path.exists():
            return default or {}
        try:
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                return json.loads(await f.read())
        except (json.JSONDecodeError, Exception) as e:
            logger.error("Ошибка чтения JSON %s: %s", file_path, str(e))
            return default or {}

    @staticmethod
    async def write_json(file_path: Path, data: Dict) -> None:
        """Асинхронно записывает данные в JSON-файл."""
        try:
            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            logger.error("Ошибка записи JSON %s: %s", file_path, str(e))
            raise HTTPException(status_code=500, detail="Ошибка сохранения данных")

    @staticmethod
    async def check_status() -> Dict[str, str]:
        """Проверяет наличие шаблонов в файловой системе."""
        templates = [f.stem for f in TEMPLATES_DIR.glob("*.docx")]
        status = "ready" if templates else "need_setup"
        logger.info("Статус проверки: %s, найдено шаблонов: %d", status, len(templates))
        return {
            "status": status,
            "message": f"{'Найден хотя бы один шаблон' if templates else 'Необходима настройка шаблонов'}",
        }

    @staticmethod
    async def start_setup() -> Dict[str, str]:
        """Запускает процесс настройки шаблонов."""
        logger.info("Начало настройки шаблонов")
        return {
            "status": "setup_started",
            "message": "Создайте поля и загрузите шаблоны",
        }

    @staticmethod
    async def define_fields(fields: List[str]) -> Dict[str, str]:
        """Сохраняет список динамических полей."""
        await TemplateManager.write_json(FIELDS_FILE, {"fields": fields})
        logger.info("Динамические поля сохранены: %s", fields)
        return {"message": "Динамические поля сохранены"}

    @staticmethod
    async def get_instruction() -> Dict[str, List[str]]:
        """Возвращает список динамических полей."""
        data = await TemplateManager.read_json(FIELDS_FILE)
        fields = data.get("fields", [])
        logger.info("Получены инструкции: %s", fields)
        return {"fields": fields}

    @classmethod
    async def list_templates(cls, db: AsyncSession) -> List[Dict[str, Any]]:
        """Получает список всех шаблонов."""
        try:
            result = await db.execute(
                select(Template).order_by(Template.created_at.desc())
            )
            templates = result.scalars().all()

            return [
                {
                    "id": template.id,
                    "template_type": template.template_type,
                    "display_name": template.display_name,
                    "fields": template.fields if template.fields else [],
                    "created_at": template.created_at,
                    "updated_at": template.updated_at,
                }
                for template in templates
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    async def initialize_templates_for_user(user_id: int, db: AsyncSession) -> None:
        """Инициализирует стандартные шаблоны для пользователя."""
        for tpl in REQUIRED_TEMPLATES:
            file_path = TEMPLATES_DIR / f"{tpl}.docx"
            template_record = Template(
                name=tpl,
                display_name=DEFAULT_DISPLAY_NAMES.get(tpl, tpl),
                file_path=str(file_path),
                user_id=user_id,
                dynamic_fields=DEFAULT_DYNAMIC_FIELDS.get(tpl, []),
            )
            db.add(template_record)
            logger.info("Добавлен шаблон %s для пользователя %d", tpl, user_id)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(
                "Ошибка инициализации шаблонов для пользователя %d: %s", user_id, str(e)
            )
            raise HTTPException(status_code=500, detail="Ошибка инициализации шаблонов")

    @classmethod
    async def delete_template(cls, db: AsyncSession, template_id: int) -> None:
        """Удаляет шаблон по ID."""
        try:
            logger.debug("Attempting to delete template: %d", template_id)

            # Get template
            template = await db.get(Template, template_id)
            if not template:
                logger.error("Template not found: %d", template_id)
                raise ValueError(f"Template with ID {template_id} not found")

            # Delete file if exists
            if template.file_path:
                try:
                    file_path = Path(template.file_path)
                    if file_path.exists():
                        file_path.unlink()
                        logger.info("Deleted template file: %s", template.file_path)
                except Exception as e:
                    logger.warning("Failed to delete template file: %s", str(e))

            # Delete from database
            await db.delete(template)
            await db.commit()

            logger.info("Successfully deleted template: %d", template_id)

        except Exception as e:
            await db.rollback()
            logger.error("Failed to delete template: %s", str(e), exc_info=True)
            raise

    @classmethod
    async def create_template(cls, db: AsyncSession, template_data: Dict[str, Any]) -> Template:
        """Создает новый шаблон."""
        try:
            # Validate required fields
            if not template_data.get("template_type"):
                raise ValueError("Template type is required")

            if not template_data.get("display_name"):
                raise ValueError("Display name is required")

            # Handle file upload if present
            file = template_data.get("file")
            file_path = None
            if file:
                file_path = await cls._save_template_file(file)

            # Ensure fields is a list
            fields = template_data.get("fields", [])
            if not isinstance(fields, list):
                fields = []

            # Create new template instance without passing a 'name' field
            new_template = Template(
                template_type=template_data["template_type"],
                display_name=template_data["display_name"],
                fields=fields,
                file_path=file_path,
                user_id=template_data.get("user_id"),
            )

            db.add(new_template)
            await db.commit()
            await db.refresh(new_template)

            return new_template

        except Exception as e:
            await db.rollback()
            raise


    @classmethod
    async def _save_template_file(cls, file: UploadFile) -> str:
        """Save uploaded template file and return its path."""
        try:
            logger.debug("Starting file save for: %s", file.filename)

            # Create unique filename
            filename = f"{uuid4()}_{file.filename}"
            file_path = TEMPLATES_DIR / filename

            # Ensure directory exists
            TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

            # Log file details
            logger.debug(
                "File details - Size: %d, Content-Type: %s",
                file.size if hasattr(file, "size") else -1,
                file.content_type,
            )

            # Save file with progress logging
            content = await file.read()
            logger.debug("Read %d bytes from uploaded file", len(content))

            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)

            logger.info("Successfully saved file to: %s", file_path)
            return str(file_path)

        except Exception as e:
            logger.error(
                "Failed to save file %s: %s", file.filename, str(e), exc_info=True
            )
            raise ValueError(f"Failed to save file {file.filename}: {str(e)}")


def unique_order(items: List[str]) -> List[str]:
    """Удаляет дубликаты, сохраняя порядок."""
    seen = set()
    return [
        item
        for item in items
        if item and item.strip() and not (item in seen or seen.add(item))
    ]
