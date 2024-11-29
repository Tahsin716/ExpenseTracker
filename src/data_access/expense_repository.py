import datetime

from src.data_access.data_access import DataAccess
from src.data_access.models.expense import Expense


class ExpenseRepository(DataAccess):

    def __init__(self):
        super().__init__()

    def add_expense(self, category_id : int, amount : float, description : str, date: datetime) -> Expense:
        try:
            expense = Expense(
                category_id=category_id,
                amount=amount,
                description=description,
                date= date
            )
            self.session.add(expense)
            self.session.commit()
            return expense
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_expenses(self) -> list[Expense]:
        return self.session.query(Expense).all()
