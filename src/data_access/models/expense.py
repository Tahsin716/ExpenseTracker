import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship

from src.data_access.models.base import Base


class Expense(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    category = relationship("Category", back_populates="expenses")