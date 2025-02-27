"""
Service layer initialization and exports.
"""

from .service_init import service_registry

# Export service instances
contract_service = service_registry.get("contract")
addendum_service = service_registry.get("addendum")
appendix_service = service_registry.get("appendix")
invoice_service = service_registry.get("invoice")
payment_service = service_registry.get("payment")
template_service = service_registry.get("template")
pdf_service = service_registry.get("pdf")
stats_service = service_registry.get("stats")
exchange_rate_service = service_registry.get("exchange_rate")

__all__ = [
    "service_registry",
    "contract_service",
    "addendum_service",
    "appendix_service",
    "invoice_service",
    "payment_service",
    "template_service",
    "pdf_service",
    "stats_service",
    "exchange_rate_service",
]
