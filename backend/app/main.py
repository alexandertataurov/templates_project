"""
FastAPI application factory and configuration.
"""

import logging
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.routers import (
    template_router,
    contract_router,
    addendum_router,
    stats_router,
    specification_router,
    appendix_router,
    exchange_rate_router,
    invoice_router,
    pdf_router,
    admin_router,
)

logger = logging.getLogger(__name__)


def register_routes(app: FastAPI) -> None:
    """Register all application routers."""
    routers = [
        template_router,
        contract_router,
        addendum_router,
        stats_router,
        specification_router,
        appendix_router,
        exchange_rate_router,
        invoice_router,
        pdf_router,
        admin_router,
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
        title="Contracts API",
        description="API for managing contracts and related documents",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
