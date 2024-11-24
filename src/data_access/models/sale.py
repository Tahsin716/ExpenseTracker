import datetime

from sqlalchemy import Integer, Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)

    sale_items = relationship("SaleItem", back_populates="sale")
    customer = relationship("Customer", back_populates="sales")