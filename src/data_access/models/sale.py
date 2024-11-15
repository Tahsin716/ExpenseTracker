from datetime import datetime

from sqlalchemy import Integer, Column, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale")