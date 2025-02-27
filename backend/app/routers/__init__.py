"""
Router initialization and configuration.
"""

from fastapi import APIRouter
from .addendum import router as addendum_router
from .admin import router as admin_router
from .appendix import router as appendix_router
from .contract import router as contract_router
from .exchange_rate import router as exchange_rate_router
from .invoice import router as invoice_router
from .payment import router as payment_router
from .pdf import router as pdf_router
from .specification import router as specification_router
from .stats import router as stats_router
from .template import router as template_router

# Create main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(contract_router)
api_router.include_router(addendum_router)
api_router.include_router(appendix_router)
api_router.include_router(invoice_router)
api_router.include_router(payment_router)
api_router.include_router(specification_router)
api_router.include_router(pdf_router)
api_router.include_router(stats_router)
api_router.include_router(exchange_rate_router)
api_router.include_router(template_router)
api_router.include_router(admin_router)

__all__ = ["api_router"]
