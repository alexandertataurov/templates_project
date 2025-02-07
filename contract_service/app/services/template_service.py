import json
import logging
from pathlib import Path
from typing import Dict, List

import aiofiles
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.template import Template

# === Конфигурация путей ===
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
GENERATED_DIR = BASE_DIR / "assets" / "generated_docs"
FIELDS_FILE = TEMPLATES_DIR / "fields.json"
PRESETS_FILE = BASE_DIR / "assets" / "presets.json"

# Разрешённые типы шаблонов
REQUIRED_TEMPLATES = ["contract", "specification", "addendum"]

# Стандартный набор динамических полей для каждого шаблона
DEFAULT_DYNAMIC_FIELDS = {
    "contract": ["date", "buyer", "seller"],
    "specification": ["date", "product_list", "total_amount"],
    "addendum": ["date", "notes"],
}

# Стандартные пользовательские названия шаблонов
DEFAULT_DISPLAY_NAMES = {
    "contract": "Стандартный договор",
    "specification": "Стандартная спецификация",
    "addendum": "Стандартное дополнение",
}

# Создаем необходимые директории (с родительскими каталогами)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemplateManager:
    """Сервис для работы с шаблонами, пресетами и их инициализацией в БД"""

    @staticmethod
    async def read_json(file_path: Path, default=None) -> Dict:
        """Асинхронно читает JSON-файл и возвращает данные или значение по умолчанию."""
        if file_path.exists():
            try:
                async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                    contents = await f.read()
                return json.loads(contents)
            except json.JSONDecodeError:
                logger.error(f"Ошибка декодирования JSON: {file_path}")
                return default or {}
            except Exception as e:
                logger.error(f"Ошибка чтения JSON: {file_path} - {str(e)}")
                return default or {}
        return default or {}

    @staticmethod
    async def write_json(file_path: Path, data: Dict):
        """Асинхронно записывает данные в JSON-файл."""
        try:
            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            logger.error(f"Ошибка записи JSON: {file_path} - {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка сохранения данных")

    @staticmethod
    async def check_status() -> Dict[str, str]:
        """
        Проверяет, загружен ли хотя бы один шаблон в файловой системе.
        Если да, возвращает статус "ready", иначе — "need_setup".
        """
        templates = [f.stem for f in TEMPLATES_DIR.glob("*.docx")]
        if templates:
            logger.info(f"Найдено {len(templates)} шаблон(ов): {templates}")
            return {"status": "ready", "message": "Найден хотя бы один шаблон"}
        logger.info("Шаблоны не найдены")
        return {"status": "need_setup", "message": "Необходима настройка шаблонов"}

    @staticmethod
    async def start_setup() -> Dict[str, str]:
        """Запускает процесс настройки шаблонов."""
        logger.info("Запущен процесс настройки шаблонов")
        return {
            "status": "setup_started",
            "message": "Создайте динамические поля и загрузите шаблоны",
        }

    @staticmethod
    async def define_fields(fields: List[str]) -> Dict[str, str]:
        """Сохраняет список динамических полей в JSON-файл."""
        await TemplateManager.write_json(FIELDS_FILE, {"fields": fields})
        logger.info("Динамические поля сохранены в JSON")
        return {"message": "Динамические поля сохранены"}

    @staticmethod
    async def get_instruction() -> Dict[str, List[str]]:
        """
        Возвращает список динамических полей из файла FIELDS_FILE.
        Окончательное форматирование поручается фронтенду.
        """
        data = await TemplateManager.read_json(FIELDS_FILE, {})
        fields = data.get("fields", [])
        logger.info(f"Инструкция (динамические поля): {fields}")
        return {"fields": fields}

    @staticmethod
    async def upload_template(
        file, template_type: str, display_name: str, db: AsyncSession
    ) -> Dict[str, str]:
        """
        Загружает шаблон DOCX в папку TEMPLATES_DIR и сохраняет в БД.
        """
        if template_type not in REQUIRED_TEMPLATES:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимый тип шаблона. Разрешены: {REQUIRED_TEMPLATES}",
            )

        safe_display_name = "_".join(display_name.strip().split())
        file_name = f"{template_type}_{safe_display_name}.docx"
        file_path = TEMPLATES_DIR / file_name

        try:
            content = await file.read()
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)
            print(f"Шаблон '{template_type}' загружен в {file_path}")

            # ✅ Добавляем запись в БД
            template_record = Template(
                name=template_type,
                display_name=display_name,
                file_path=str(file_path),
                dynamic_fields=[],  # Если есть поля, добавь их сюда
                user_id=None,  # Если у тебя есть пользователи, сюда передаётся ID
            )

            db.add(template_record)
            await db.commit()
            print(f"Шаблон {template_type} сохранён в БД")

            return {"message": f"Шаблон '{display_name}' загружен и сохранён!"}

        except Exception as e:
            print(f"Ошибка загрузки шаблона: {str(e)}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="Ошибка загрузки файла")

    @staticmethod
    async def list_templates(db: AsyncSession) -> List[Dict]:
        """
        Запрашивает из базы данных все шаблоны и возвращает их полную информацию.
        """
        result = await db.execute(select(Template))
        templates = result.scalars().all()
        # Преобразуем каждый объект Template в словарь
        templates_info = [
            {
                "id": template.id,
                "type": template.name,  # тип шаблона
                "display_name": template.display_name,
                "file_path": template.file_path,
                "dynamic_fields": template.dynamic_fields,
                "created_at": (
                    template.created_at.isoformat() if template.created_at else None
                ),
                "user_id": template.user_id,
            }
            for template in templates
        ]
        logger.info(f"Список шаблонов (БД): {templates_info}")
        return templates_info

    @staticmethod
    async def initialize_templates_for_user(user_id: int, db: AsyncSession) -> None:
        """
        Инициализирует стандартный набор шаблонов для нового пользователя.
        Для каждого шаблона задается стандартный тип, отображаемое имя и динамические поля.
        """
        for tpl in REQUIRED_TEMPLATES:
            file_path = TEMPLATES_DIR / f"{tpl}.docx"
            dynamic_fields = DEFAULT_DYNAMIC_FIELDS.get(tpl, [])
            display_name = DEFAULT_DISPLAY_NAMES.get(tpl, tpl)
            template_record = Template(
                name=tpl,
                display_name=display_name,
                file_path=str(file_path),
                user_id=user_id,
                dynamic_fields=dynamic_fields,
            )
            db.add(template_record)
            logger.info(
                f"Подготовлена запись для шаблона '{tpl}' с названием '{display_name}' и полями {dynamic_fields}"
            )
        try:
            await db.commit()
            logger.info(
                f"Стандартные шаблоны инициализированы для пользователя {user_id}"
            )
        except Exception as e:
            await db.rollback()
            logger.error(
                f"Ошибка инициализации шаблонов для пользователя {user_id}: {str(e)}"
            )
            raise HTTPException(status_code=500, detail="Ошибка инициализации шаблонов")

    @staticmethod
    async def upload_template(
        file, template_type: str, display_name: str, fields: List[str], db: AsyncSession
    ) -> Dict[str, str]:
        """
        Асинхронно загружает шаблон DOCX в папку TEMPLATES_DIR и сохраняет в БД.
        """
        if template_type not in REQUIRED_TEMPLATES:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимый тип шаблона. Разрешены: {REQUIRED_TEMPLATES}",
            )

        safe_display_name = "_".join(display_name.strip().split())
        file_name = f"{template_type}_{safe_display_name}.docx"
        file_path = TEMPLATES_DIR / file_name

        try:
            content = await file.read()
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(content)
            logger.info(f"Шаблон '{template_type}' загружен в {file_path}")

            # ✅ Добавляем запись в БД с dynamic_fields
            template_record = Template(
                name=template_type,
                display_name=display_name,
                file_path=str(file_path),
                dynamic_fields=fields,  # <-- Исправлено: сохраняем переданные поля
                user_id=None,
            )

            db.add(template_record)
            await db.commit()
            logger.info(f"Шаблон {template_type} сохранён в БД с полями: {fields}")

            return {"message": f"Шаблон '{display_name}' загружен и сохранён!"}

        except Exception as e:
            logger.error(f"Ошибка загрузки шаблона: {str(e)}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="Ошибка загрузки файла")

    @staticmethod
    async def delete_template(
        template_type: str, display_name: str, db: AsyncSession
    ) -> Dict[str, str]:
        """
        Удаляет шаблон по типу и пользовательскому названию.
        Формирует имя файла так же, как при загрузке.
        """
        safe_display_name = "_".join(display_name.strip().split())
        file_name = f"{template_type}_{safe_display_name}.docx"
        file_path = TEMPLATES_DIR / file_name
        if not file_path.exists():
            logger.error(f"Шаблон '{display_name}' не найден для удаления")
            raise HTTPException(status_code=404, detail="Шаблон не найден")
        try:
            file_path.unlink()
            logger.info(f"Шаблон '{display_name}' удален из {file_path}")
            return {"message": f"Шаблон '{display_name}' удален!"}
        except Exception as e:
            logger.error(f"Ошибка удаления шаблона '{display_name}': {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка удаления шаблона")

    @staticmethod
    async def update_template(template_id: int, updated_data: dict, db: AsyncSession):
        """
        Обновляет шаблон, изменяя только разрешенные параметры.
        Запрещено изменять: file_path, user_id.
        :param template_id: ID шаблона в БД
        :param updated_data: Словарь с обновляемыми данными
        :param db: Асинхронная сессия SQLAlchemy
        :return: Подтверждающее сообщение
        """
        # Запрещенные поля
        forbidden_fields = {"file_path", "user_id"}

        # Фильтруем запрещенные поля
        filtered_data = {
            k: v for k, v in updated_data.items() if k not in forbidden_fields
        }

        if not filtered_data:
            logger.warning(
                f"Нет разрешенных данных для обновления шаблона ID {template_id}"
            )
            raise HTTPException(
                status_code=400,
                detail="Нет данных для обновления или запрещено изменять указанные поля.",
            )

        async with db.begin():
            result = await db.execute(
                select(Template).where(Template.id == template_id)
            )
            template = result.scalars().first()

            if not template:
                logger.error(f"Шаблон с ID {template_id} не найден.")
                raise HTTPException(status_code=404, detail="Шаблон не найден")

            # Обновляем только разрешенные параметры
            for key, value in filtered_data.items():
                setattr(template, key, value)

            await db.commit()
            logger.info(f"Шаблон ID {template_id} обновлён: {filtered_data}")

        return {"message": f"Шаблон ID {template_id} успешно обновлён!"}
