from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import contract, addendum, stats, specification, appendix, exchange_rate, invoice, pdf, template
import logging
import uvicorn



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Самый Крутой Бэк",
    description="Бэкэнд для управления договорами, счетами, платежами и шаблонами",
    version="1.0.0",
)

# Добавляем CORS для поддержки запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

