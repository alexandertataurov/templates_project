from app.models.base import Base
from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.specification import Specification
from app.models.addendum import Addendum
from app.models.appendix import Appendix
from app.models.template import Template


from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy"""

    pass
