from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    reorder_level = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sale_items = relationship("SaleItem", back_populates="item")