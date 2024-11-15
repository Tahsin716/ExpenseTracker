from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    expenses = relationship("Expense", back_populates="category")