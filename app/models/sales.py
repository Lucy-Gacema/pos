from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base

class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0)
    payment_status = Column(String, nullable=False)
    receipt_number = Column(
        String, ForeignKey("receipts.receipt_number"), nullable=False, unique=True
    )
    sale_date = Column(DateTime, nullable=False)

    user = relationship("User")
    customer = relationship("Customer")
    receipt = relationship("Receipt")