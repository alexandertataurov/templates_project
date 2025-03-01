"""
FastAPI application factory and configuration.
"""

import logging
import os
from dotenv import load_dotenv
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings  # Updated import
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.routers import (
    documents_router,
    stats_router,
    pdf_router,
    admin_router,
    template_router,
)

# Load .env explicitly before imports (optional if already in config.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)

logger = logging.getLogger(__name__)


def register_routes(app: FastAPI) -> None:
    """Register all application routers."""
    routers = [
        documents_router,
        stats_router,
        pdf_router,
        admin_router,
        template_router,
    ]
    for router in routers:
        app.include_router(router)
        logger.debug(
            "Registered router: %s", router.tags[0] if router.tags else "Unnamed"
        )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Initialize logging
    setup_logging()

    # Create FastAPI instance
    app = FastAPI(
        title=settings.project_name,
        description="API for managing contracts and related documents",
        version=settings.version,
        docs_url="/docs" if settings.DEBUG else None,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Register routes
    register_routes(app)

    # Setup middlewares
    setup_middleware(app)

    return app


# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server with DEBUG=%s", settings.DEBUG)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
