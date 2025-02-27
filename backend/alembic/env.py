import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

from app.database import engine
from app.models import Base
from app.config import settings

# Alembic Config object
config = context.config

# Override sqlalchemy.url with value from settings if not explicitly set
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Interpret the config file for logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Compare column types
        compare_server_default=True,  # Compare server defaults
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async support."""
    try:
        async with engine.begin() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"Error during migration: {e}")
        raise


def do_run_migrations(connection):
    """Run migrations in a sync context."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
