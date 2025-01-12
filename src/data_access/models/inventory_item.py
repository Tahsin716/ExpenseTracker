import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String)
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    sale_items = relationship("SaleItem", back_populates="item")