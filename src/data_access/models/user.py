import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    role = Column(String(50), nullable=False)

    expenses = relationship("Expense", back_populates="user")
    sales = relationship("Sale", back_populates="user")