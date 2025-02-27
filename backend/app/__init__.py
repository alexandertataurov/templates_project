"""
Core application initialization.
Exports main configuration and logging components.
"""

from app.config import settings
from app.logger import setup_logging

# Initialize logging at startup
setup_logging()

__all__ = ["settings", "setup_logging"]
