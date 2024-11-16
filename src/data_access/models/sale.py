import datetime

from sqlalchemy import Integer, Column, String, Float, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    customer_phone_number = Column(String(20))

    sale_items = relationship("SaleItem", back_populates="sales")
    customers = relationship("Customer", back_populates="sales")