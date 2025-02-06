from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Specification(Base):
    __tablename__ = "specifications"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, index=True)
    spec_number = Column(String(50), nullable=False, index=True)
    spec_date = Column(Date, nullable=False)
    goods_description = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)

    contract = relationship("Contract", back_populates="specifications")
