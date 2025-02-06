from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, nullable=False, index=True)
    contract_date = Column(Date, nullable=False)
    place_of_signing = Column(String(255), nullable=False)
    valid_date = Column(Date, nullable=True)

    supplier_name = Column(String(255), nullable=False)
    supplier_representative = Column(String(255), nullable=False)

    supplier_address = Column(String(255), nullable=False)
    supplier_inn = Column(String(50), nullable=True)
    supplier_bik = Column(String(50), nullable=True)
    supplier_ogrn = Column(String(50), nullable=True)
    supplier_bank = Column(String(255), nullable=False)
    supplier_swift = Column(String(50), nullable=True)
    supplier_account = Column(String(50), nullable=False)

    buyer_name = Column(String(255), nullable=False)
    buyer_address = Column(String(255), nullable=False)
    buyer_bank = Column(String(255), nullable=False)
    buyer_swift = Column(String(50), nullable=True)
    buyer_account = Column(String(50), nullable=False)
    buyer_tax_id = Column(String(50), nullable=False)

    goods_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)
    payment_date = Column(Date, nullable=False)

    currency = Column(String(10), nullable=False, default="CNY")
    exchange_rate = Column(Numeric(10, 4), nullable=True)
    delivery_terms = Column(String(50), nullable=False, default="CIF Владивосток")
    incoterms = Column(String(50), nullable=False, default="Incoterms 2020")
    claim_period = Column(Integer, nullable=False, default=20)
    response_period = Column(Integer, nullable=False, default=14)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    specifications = relationship("Specification", back_populates="contract", cascade="all, delete-orphan")
    addendums = relationship("Addendum", back_populates="contract", cascade="all, delete-orphan")
    appendices = relationship("Appendix", back_populates="contract", cascade="all, delete-orphan", passive_deletes=True)
    invoices = relationship("Invoice", back_populates="contract", cascade="all, delete-orphan")
