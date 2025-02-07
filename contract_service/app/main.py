import logging
import sys
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .config import settings
from .routers import (
    contract,
    addendum,
    stats,
    specification,
    appendix,
    exchange_rate,
    invoice,
    pdf,
    template,
    admin,
)

# Настройка логирования
log_file = settings.LOG_FILE
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logging.getLogger("fastapi").addHandler(file_handler)
logging.getLogger("uvicorn.access").addHandler(file_handler)
logging.getLogger("uvicorn.error").addHandler(file_handler)

# Инициализация FastAPI
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


# Middleware для отладки
class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if settings.DEBUG:
            response.headers["X-Debug-Mode"] = "Enabled"
        return response


app.add_middleware(DebugMiddleware)


# Глобальные обработчики ошибок
@app.exception_handler(404)
async def not_found_error_handler(request: Request, exc):
    logger.error(f"❌ 404 Not Found: {request.url}")
    return JSONResponse(status_code=404, content={"error": "Not Found"})


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):
    logger.error(f"🔥 500 Internal Server Error: {request.url} - {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Ошибка: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "message": "Что-то пошло не так"},
    )


# Маршруты
app.include_router(contract.router)
app.include_router(addendum.router)
app.include_router(stats.router)
app.include_router(specification.router)
app.include_router(appendix.router)
app.include_router(exchange_rate.router)
app.include_router(invoice.router)
app.include_router(pdf.router)
app.include_router(template.router)
app.include_router(admin.router)


# Проверка состояния API
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/debug")
def debug_info():
    logger.debug("Запрос на debug")
    return (
        {"debug_info": "Debug mode is active"}
        if settings.DEBUG
        else {"message": "Debug is off"}
    )


# Сбор статистики API
api_stats = {
    "total_requests": 0,
    "error_400": 0,
    "error_500": 0,
    "average_response_time": 0.0,
    "top_endpoints": defaultdict(int),
    "requests_per_minute": defaultdict(int),
}


@app.middleware("http")
async def api_stats_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time

    api_stats["total_requests"] += 1
    api_stats["average_response_time"] = (
        api_stats["average_response_time"] * (api_stats["total_requests"] - 1)
        + response_time
    ) / api_stats["total_requests"]

    endpoint = request.url.path
    api_stats["top_endpoints"][endpoint] += 1

    if 400 <= response.status_code < 500:
        api_stats["error_400"] += 1
    elif response.status_code >= 500:
        api_stats["error_500"] += 1

    return response


logger.info("✅ Сервер запущен! Логи пишутся в %s", log_file)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
