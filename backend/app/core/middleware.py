"""
Application middleware configuration.
"""

import time
import logging
from collections import defaultdict
from typing import Callable, Dict, Any
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.config import settings

logger = logging.getLogger(__name__)


class DebugMiddleware(BaseHTTPMiddleware):
    """Middleware to add debug headers and logging in DEBUG mode."""

    async def dispatch(self, request: Request, call_next: Callable) -> Request:
        start_time = time.time()
        response = await call_next(request)

        if settings.DEBUG:
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Debug-Mode"] = "Enabled"
            logger.debug(
                "Request: %s %s - Time: %.3fs",
                request.method,
                request.url.path,
                process_time,
            )

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for request validation and preprocessing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process incoming request.

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response object
        """
        # Add request validation logic here
        return await call_next(request)


class ResponseValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for response validation and postprocessing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate and process response."""
        response = await call_next(request)
        # Add response validation logic here
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle errors globally."""
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})


def setup_middleware(app: FastAPI) -> None:
    """Configure application middleware."""
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(ResponseValidationMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    # Add debug middleware in debug mode
    if settings.DEBUG:
        app.add_middleware(DebugMiddleware)
        logger.debug("Debug middleware enabled")

    # Request statistics
    stats = {
        "total_requests": 0,
        "errors": defaultdict(int),
        "endpoints": defaultdict(int),
    }

    @app.middleware("http")
    async def stats_middleware(request: Request, call_next: Callable) -> Request:
        """Collect request statistics."""
        stats["total_requests"] += 1
        stats["endpoints"][request.url.path] += 1

        response = await call_next(request)

        if response.status_code >= 400:
            stats["errors"][response.status_code] += 1

        return response
