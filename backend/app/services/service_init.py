"""
Centralized service initialization and management.
"""

import logging
from typing import Dict, Any

from .addendum_service import AddendumService
from .appendix_service import AppendixService
from .contract_service import ContractService
from .exchange_rate_service import ExchangeRateService
from .invoice_service import InvoiceService
from .payment_service import PaymentService
from .pdf_service import PDFService
from .stats_service import StatsService
from .template_service import TemplateManager

from app.models import Contract, Addendum, Appendix, Invoice, Payment

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Registry for all application services."""

    def __init__(self):
        """Initialize all services."""
        self.services: Dict[str, Any] = {}
        self._initialize_services()

    def _initialize_services(self) -> None:
        """Initialize all service instances."""
        try:
            # Initialize core services
            self.services.update(
                {
                    "contract": ContractService(Contract),
                    "addendum": AddendumService(Addendum),
                    "appendix": AppendixService(Appendix),
                    "invoice": InvoiceService(Invoice),
                    "payment": PaymentService(Payment),
                    "template": TemplateManager(),
                }
            )

            # Initialize utility services
            self.services.update(
                {
                    "pdf": PDFService(),
                    "stats": StatsService(),
                    "exchange_rate": ExchangeRateService(),
                }
            )

            logger.info("All services initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize services: %s", str(e), exc_info=True)
            raise

    def get(self, service_name: str) -> Any:
        """Get a service instance by name."""
        if service_name not in self.services:
            raise KeyError(f"Service '{service_name}' not found")
        return self.services[service_name]


# Create global service registry
service_registry = ServiceRegistry()
