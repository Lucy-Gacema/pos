from sqlalchemy import(
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base

class Payment(Base):
    __tablename__="payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"),nullable=False)
    payment_method = Column(String, nullable=False)
    amount_paid = Column(Numeric(10,2), nullable=False)
    payment_date = Column(DateTime, nullable=False)

    sale = relationship("Sale")


    