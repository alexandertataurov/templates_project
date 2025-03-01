"""
Centralized service initialization and management.
"""

import logging
from typing import Dict, Any

from .document_service import DocumentService
from .pdf_service import PDFService
from .stats_service import StatsService
from .template_manager import TemplateManager
from app.models.document import Document

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
            self.services.update(
                {
                    "document": DocumentService(Document),
                    "template": TemplateManager(),
                    "pdf": PDFService(),
                    "stats": StatsService(),
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
