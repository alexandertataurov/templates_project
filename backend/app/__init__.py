"""
Core application initialization.
Exports main configuration and logging components.
"""

from app.core.config import settings
from app.core.logging import setup_logging

# Initialize logging at startup
setup_logging()

__all__ = ["settings", "setup_logging"]
