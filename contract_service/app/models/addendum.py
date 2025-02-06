from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Addendum(Base):
    __tablename__ = "addendums"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, index=True)  # Индексируем contract_id
    addendum_number = Column(String(50), nullable=False, index=True)  # Индексируем номер ДС
    addendum_date = Column(Date, nullable=False)
    invoice_number = Column(String(50), nullable=True, index=True)  # Индексируем инвойс
    invoice_amount = Column(Numeric(15, 2), nullable=True)
    exchange_rate = Column(Numeric(10, 4), nullable=True)
    description = Column(String(255), nullable=True)

    contract = relationship("Contract", back_populates="addendums")
