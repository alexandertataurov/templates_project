from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class Appendix(Base):
    __tablename__ = "appendices"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(
        Integer, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False
    )
    appendix_number = Column(String(50), nullable=False)
    appendix_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    contract = relationship(
        "Contract", back_populates="appendices", passive_deletes=True
    )
