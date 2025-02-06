import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

from app.database import engine  # Используем наш асинхронный engine
from app.models import Base  # Подключаем модели

# Конфигурация Alembic
config = context.config

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем метаданные моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в онлайн-режиме с асинхронным движком."""
    async with engine.begin() as connection:
        await connection.run_sync(do_migrations)


def do_migrations(connection):
    """Функция, выполняющая миграции в синхронном контексте."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run():
    """Запускает миграции синхронно, вызывая асинхронную функцию."""
    asyncio.run(run_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run()
