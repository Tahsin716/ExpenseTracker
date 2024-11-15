from datetime import datetime

from src.data_access.data_access import DataAccess
from src.data_access.models.expense import Expense


class ExpenseRepository(DataAccess):

    def __init__(self):
        super().__init__()

    def add_expense(self, user_id : str, category_id : str, amount : int | float, description : str, date: datetime|None) -> Expense:
        try:
            expense = Expense(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                description=description,
                date=date
            )
            self.session.add(expense)
            self.session.commit()
            return expense
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_expenses(self, user_id : str, start_date : datetime|None = None, end_date : datetime|None = None) -> Expense:
        query = self.session.query(Expense).filter_by(user_id=user_id)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        return query.all()
