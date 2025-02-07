"""
Модуль API для мониторинга бэкенда.
"""

import logging
import psutil
import os
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
# from app.models.user import User
from sqlalchemy.future import select

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
async def get_logs(level: str = "ERROR"):
    """Возвращает последние ошибки логирования."""
    log_file_path = "server.log"
    if not os.path.exists(log_file_path):
        return {"logs": "Лог-файл не найден."}

    with open(log_file_path, "r", encoding="utf-8") as log_file:
        logs = [line.strip() for line in log_file.readlines() if level in line]
    return {"logs": logs[-10:]}  # Возвращаем последние 10 записей

# ✅ 3. Статистика API
@router.get("/api/stats")
async def api_stats():
    """Возвращает статистику API (заглушка)."""
    return {
        "total_requests": 1524,
        "error_rate": "5%",
        "average_response_time": "120ms",
        "top_endpoints": ["/users", "/orders", "/products"],
    }

# ✅ 4. Проверка состояния базы данных
@router.get("/db/status")
async def db_status(db: AsyncSession = Depends(get_db)):
    """Проверяет подключение к базе данных."""
    try:
        await db.execute(select(1))
        return {"database": "Connected"}
    except Exception as e:
        logger.error("Ошибка подключения к БД: %s", str(e))
        return {"database": "Disconnected", "error": str(e)}

# ✅ 5. Активные пользователи
'''
@router.get("/users/online")
async def users_online(db: AsyncSession = Depends(get_db)):
    """Возвращает количество активных пользователей (пример)."""
    result = await db.execute(select(User).where(User.is_active == True))
    users = result.scalars().all()
    return {"active_users": len(users)}
'''

# ✅ 6. Статус фоновых задач
@router.get("/tasks/status")
async def tasks_status():
    """Возвращает статус фоновых задач (заглушка)."""
    return {
        "running_tasks": 3,
        "failed_tasks": 1,
        "last_task_time": "2m ago",
    }

# ✅ 7. Конфигурация сервера
@router.get("/config")
async def server_config():
    """Возвращает текущие переменные окружения и настройки."""
    return {
        "python_version": os.popen("python --version").read().strip(),
        "fastapi_version": "0.100.0",
        "database_url": os.getenv("DATABASE_URL", "Not Set"),
        "debug_mode": os.getenv("DEBUG", "false"),
    }
