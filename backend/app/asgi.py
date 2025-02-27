"""
ASGI application configuration for production deployment.
"""

import logging
from app.main import create_app
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI application
app = create_app()

# Log available routes in debug mode
if settings.DEBUG:
    logger.debug("Available routes:")
    for route in app.routes:
        methods = ", ".join(route.methods) if route.methods else "N/A"
        logger.debug("%s %s", methods, route.path)

# Export ASGI application
application = app
