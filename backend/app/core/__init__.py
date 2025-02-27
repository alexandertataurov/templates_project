"""
Core application functionality and configuration.
"""

from .config import Settings, get_settings
from .dependencies import get_current_user, get_current_active_user
from .events import create_start_app_handler, create_stop_app_handler
from .exceptions import APIError, NotFoundError, ValidationError, AuthenticationError
from .journal import Journal
from .logging import setup_logging, get_logger, ContextLogger
from .metrics import Metrics, timing, metrics
from .middleware import setup_middleware
from .profiler import profile
from .security import create_access_token, verify_password, get_password_hash

__all__ = [
    # Config
    "Settings",
    "get_settings",
    # Dependencies
    "get_current_user",
    "get_current_active_user",
    # Event handlers
    "create_start_app_handler",
    "create_stop_app_handler",
    # Exceptions
    "APIError",
    "NotFoundError",
    "ValidationError",
    "AuthenticationError",
    # Journal
    "Journal",
    # Logging
    "setup_logging",
    "get_logger",
    "ContextLogger",
    # Metrics
    "Metrics",
    "timing",
    "metrics",
    # Middleware
    "setup_middleware",
    "RequestValidationMiddleware",
    "ResponseValidationMiddleware",
    "ErrorHandlingMiddleware",
    # Profiler
    "profile",
    # Security
    "create_access_token",
    "verify_password",
    "get_password_hash",
]
