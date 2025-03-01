"""
Router initialization and configuration.
"""

from fastapi import APIRouter
from .documents import router as documents_router
from .admin import router as admin_router
from .pdf import router as pdf_router
from .stats import router as stats_router
from .template import router as template_router

# Create main API router
api_router = APIRouter()

# Include active routers
api_router.include_router(documents_router)
api_router.include_router(pdf_router)
api_router.include_router(stats_router)
api_router.include_router(template_router)
api_router.include_router(admin_router)

__all__ = ["api_router"]
