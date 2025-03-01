"""
Модуль API для мониторинга бэкенда.
"""

import logging
import psutil
import os
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)


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


@router.get("/logs")
async def get_logs():
    """Возвращает последние 10 строк логов."""
    log_file = "logs.txt"
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            logs = file.readlines()[-10:]
        return {"logs": logs}
    except FileNotFoundError:
        return {"error": "Файл логов не найден"}


@router.get("/db/status")
async def db_status(db: AsyncSession = Depends(get_db)):
    """Проверяет подключение к базе данных."""
    try:
        result = await db.execute(text("SELECT 1"))
        connections = await db.execute(text("SELECT COUNT(*) FROM pg_stat_activity"))
        return {
            "database": "Connected",
            "active_connections": connections.scalar(),
        }
    except Exception as e:
        logger.error("Ошибка подключения к БД: %s", str(e))
        return {"database": "Disconnected", "error": str(e)}


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


@router.get("/db/schema")
async def get_db_schema(db: AsyncSession = Depends(get_db)):
    """Get database schema information for debugging."""
    try:
        table_exists = await db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'documents')"
            )
        )
        table_exists = table_exists.scalar()
        columns = []
        if table_exists:
            column_info = await db.execute(
                text(
                    "SELECT column_name, data_type, is_nullable FROM information_schema.columns "
                    "WHERE table_name = 'documents'"
                )
            )
            columns = [dict(row._mapping) for row in column_info]
        return {"table_exists": table_exists, "columns": columns}
    except Exception as e:
        return {"error": str(e)}


@router.post("/db/init-documents")
async def init_documents_table(db: AsyncSession = Depends(get_db)):
    """Initialize documents table with correct schema."""
    try:
        await db.execute(text("DROP TABLE IF EXISTS documents CASCADE"))
        await db.execute(
            text(
                """
                CREATE TABLE documents (
                    id SERIAL PRIMARY KEY,
                    document_type VARCHAR(50) NOT NULL,
                    reference_number VARCHAR(50) NOT NULL,
                    created_date DATE NOT NULL,
                    dynamic_fields JSON,
                    parent_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                    CONSTRAINT uq_doc_type_ref UNIQUE (document_type, reference_number)
                )
                """
            )
        )
        await db.commit()
        return {"message": "Documents table initialized successfully"}
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
