from sqlalchemy import(
    Column,
    Integer,
    String,
    Boolean
)

from app.database import Base
class User(Base):
    __tablename__="users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False, default='cashier')
    is_active = Column(Boolean, nullable=False, default=True)
