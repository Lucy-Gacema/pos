from sqlalchemy import(
    Column,
    String,
    Boolean
)

from app.database import Base

class Receipt(Base):
    __tablename__="receipts"

    receipt_number = Column(String, primary_key=True, index=True)
    is_printed = Column(Boolean, nullable=False)


    