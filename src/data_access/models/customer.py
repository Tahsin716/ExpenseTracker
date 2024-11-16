from enum import unique

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)


    sales = relationship("Sale", back_populates="customer")