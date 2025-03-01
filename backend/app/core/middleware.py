"""
Application middleware configuration.
"""

import time
import logging
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from .config import settings
from .logging import get_logger

logger = get_logger(__name__)


class DebugMiddleware(BaseHTTPMiddleware):
    """Middleware to add debug headers and logging in DEBUG mode."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
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


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            logger.error("Unhandled exception: %s", str(e), exc_info=True)
            return JSONResponse(status_code=500, content={"detail": str(e)})


def setup_middleware(app: FastAPI) -> None:
    """Configure application middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    app.add_middleware(ErrorHandlingMiddleware)
    if settings.DEBUG:
        app.add_middleware(DebugMiddleware)
        logger.debug("Debug middleware enabled")
