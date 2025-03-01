"""
Database configuration using SQLAlchemy for async operations.
"""

from typing import AsyncGenerator, Any, Dict
from datetime import datetime
import logging
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    """Base class for all database models."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def update(self, **kwargs: Any) -> None:
        """Update model attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.

    Yields:
        AsyncSession: Active database session
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error("Database session error: %s", str(e), exc_info=True)
        await session.rollback()
        raise
    finally:
        await session.close()


# Add synchronous wrapper for FastAPI compatibility
def get_db_sync():
    """Synchronous wrapper for get_db."""
    return AsyncSessionLocal()


async def init_db() -> None:
    """Initialize database tables and indexes."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
