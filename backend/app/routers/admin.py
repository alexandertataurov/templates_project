"""
Модуль API для мониторинга бэкенда.
"""

import logging
import psutil
import os
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from app.database import get_db
from datetime import datetime

# from app.celery import celery_app
# from celery.app.control import Inspect
# from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)


# ✅ 1. Проверка статуса сервера
@router.get("/health")
async def health_check():
    """Проверяет статус сервера."""
    return {
        "status": "Online",
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
        "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ✅ 2. Получение логов
@router.get("/logs")
async def get_logs():
    """Возвращает последние 10 строк логов."""
    log_file = "logs.txt"

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            logs = file.readlines()[-10:]  # ✅ Показываем последние 10 логов
        return {"logs": logs}
    except FileNotFoundError:
        return {"error": "Файл логов не найден"}


# ✅ 2. API для получения статистики
@router.get("/api/stats")
async def get_api_stats():
    """Возвращает статистику API из `main.py`."""
    from app.main import api_stats  # ✅ Получаем данные из main.py

    return {
        "total_requests": api_stats["total_requests"],
        "error_400": api_stats["error_400"],
        "error_500": api_stats["error_500"],
        "average_response_time": f"{api_stats['average_response_time']:.2f}s",
        "top_endpoints": sorted(
            api_stats["top_endpoints"].items(), key=lambda x: x[1], reverse=True
        )[:5],
    }


# ✅ 4. Проверка состояния базы данных
@router.get("/db/status")
async def db_status(db: AsyncSession = Depends(get_db)):
    """Проверяет подключение к базе данных."""
    try:
        result = await db.execute(select(1))
        return {
            "database": "Connected",
            "active_connections": await db.execute(
                text("SELECT COUNT(*) FROM pg_stat_activity")
            ),  # ✅ Показывает активные соединения
        }
    except Exception as e:
        logger.error("Ошибка подключения к БД: %s", str(e))
        return {"database": "Disconnected", "error": str(e)}


# ✅ 5. Активные пользователи
'''
@router.get("/users/online")
async def users_online(db: AsyncSession = Depends(get_db)):
    """Возвращает количество активных пользователей."""
    result = await db.execute(select(User).where(User.is_active == True))
    users = result.scalars().all()
    return {"active_users": len(users)}
'''
# ✅ 6. Статус фоновых задач (если используется Celery)
'''
@router.get("/tasks/status")
async def tasks_status():
    """Проверяет статус фоновых задач Celery."""
    inspector = Inspect(celery_app)
    active_tasks = inspector.active() or {}
    scheduled_tasks = inspector.scheduled() or {}
    failed_tasks = inspector.reserved() or {}

    return {
        "running_tasks": sum(len(v) for v in active_tasks.values()),
        "failed_tasks": sum(len(v) for v in failed_tasks.values()),
        "scheduled_tasks": sum(len(v) for v in scheduled_tasks.values()),
    }
'''


# ✅ 7. Конфигурация сервера
@router.get("/config")
async def server_config():
    """Возвращает текущие переменные окружения и настройки."""
    return {
        "python_version": os.popen("python --version").read().strip(),
        "fastapi_version": "0.100.0",
        "database_url": os.getenv("DATABASE_URL", "Not Set"),
        "debug_mode": os.getenv("DEBUG", "false"),
        "worker_status": "Running" if os.system("pgrep -f celery") == 0 else "Stopped",
    }


@router.get("/db/schema", tags=["Admin"])
async def get_db_schema(db: AsyncSession = Depends(get_db)):
    """Get database schema information for debugging."""
    try:
        # Check if templates table exists
        table_exists = await db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'templates')"
            )
        )
        table_exists = table_exists.scalar()

        # Get column information if table exists
        columns = []
        if table_exists:
            column_info = await db.execute(
                text(
                    "SELECT column_name, data_type, is_nullable FROM information_schema.columns "
                    "WHERE table_name = 'templates'"
                )
            )
            columns = [dict(row._mapping) for row in column_info]

        return {"table_exists": table_exists, "columns": columns}
    except Exception as e:
        return {"error": str(e)}


@router.post("/db/init-templates", tags=["Admin"])
async def init_templates_table(db: AsyncSession = Depends(get_db)):
    """Initialize templates table with correct schema."""
    try:
        # Drop the table if it exists
        await db.execute(text("DROP TABLE IF EXISTS templates CASCADE"))

        # Create the table with all required columns
        await db.execute(
            text(
                """
            CREATE TABLE templates (
                id SERIAL PRIMARY KEY,
                template_type VARCHAR NOT NULL DEFAULT 'default',
                display_name VARCHAR NOT NULL DEFAULT 'Untitled',
                fields JSONB,
                file_path VARCHAR,
                user_id INTEGER,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """
            )
        )

        await db.commit()

        return {"message": "Templates table initialized successfully"}
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
