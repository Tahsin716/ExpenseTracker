from sqlalchemy import Integer, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class SaleItem(Base):
    __tablename__ = 'sale_items'

    sale_item_id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.sale_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('inventory_items.item_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="sale_items")
    item = relationship("InventoryItem", back_populates="sale_items")