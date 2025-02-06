from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime

class Base(DeclarativeBase):
    """Базовый класс моделей SQLAlchemy."""
    __abstract__ = True  

    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
