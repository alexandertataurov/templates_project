"""
Основной модуль FastAPI приложения.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .config import settings
from .routers import (
    contract, addendum, stats, specification, appendix,
    exchange_rate, invoice, pdf, template
)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Самый Крутой Бэк",
    description="Бэкэнд для управления договорами, счетами, платежами и шаблонами",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class DebugMiddleware(BaseHTTPMiddleware):
    """
    Middleware для добавления заголовка X-Debug-Mode.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Добавляет заголовок `X-Debug-Mode`, если включен Debug Mode.
        """
        response = await call_next(request)
        if settings.DEBUG:
            response.headers["X-Debug-Mode"] = "Enabled"
        return response

app.add_middleware(DebugMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик ошибок.
    """
    logger.error("Ошибка: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "message": "Что-то пошло не так"},
    )

@app.get("/health")
def health_check():
    """
    Проверка работоспособности API.
    """
    return {"status": "ok"}

@app.get("/debug")
def debug_info():
    """
    Проверка включенного Debug Mode.
    """
    logger.debug("Запрос на debug")
    return {"debug_info": "Debug mode is active"} if settings.DEBUG else {"message": "Debug is off"}

app.include_router(contract.router)
app.include_router(addendum.router)
app.include_router(stats.router)
app.include_router(specification.router)
app.include_router(appendix.router)
app.include_router(exchange_rate.router)
app.include_router(invoice.router)
app.include_router(pdf.router)
app.include_router(template.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
