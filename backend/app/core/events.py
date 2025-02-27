"""
Application event handlers.
"""

from typing import Callable
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from app.database import engine


async def close_db_connection(app: FastAPI, engine: AsyncEngine) -> None:
    """Close database connection on shutdown."""
    await engine.dispose()


def create_start_app_handler(app: FastAPI) -> Callable:
    """
    Create startup event handler.

    Args:
        app: FastAPI application instance

    Returns:
        Startup handler function
    """

    async def start_app() -> None:
        # Add startup tasks here
        pass

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    Create shutdown event handler.

    Args:
        app: FastAPI application instance

    Returns:
        Shutdown handler function
    """

    async def stop_app() -> None:
        await close_db_connection(app, engine)

    return stop_app
