import datetime
import logging
from typing import Dict, Tuple
from collections import Counter

from src.business.exception.security_exception import SecurityException

from src.business.utils.validation import Validation
from src.data_access.category_repository import CategoryRepository
from src.data_access.expense_repository import ExpenseRepository
from src.data_access.models.expense import Expense


class ExpenseManager:

    def __init__(self):
        self.expense_repository = ExpenseRepository()
        self.category_repository = CategoryRepository()
        self.validator = Validation()

    def add_expense(self, category_id: int, amount: str,
                    description: str, date_str: str) -> Tuple[bool, str, Expense]:
        try:
            description = self.validator.sanitize_input(description)
            amount = float(amount)

            if not category_id:
                raise SecurityException("Category cannot be empty")

            if not isinstance(amount, (int, float)) or amount <= 0:
                raise SecurityException("Invalid amount")

            if date_str:
                if not self.validator.validate_date_format(date_str):
                    raise SecurityException("Invalid date format, date format is YYYY-MM-DD")
                else:
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date = datetime.datetime.now(datetime.timezone.utc)

            expense = self.expense_repository.add_expense(category_id, amount, description, date)
            return True, "", expense

        except SecurityException as e:
            logging.error(f"Security error adding expense: {str(e)}")
            return False, str(e), Expense()
        except ValueError:
            return False, "Invalid amount", Expense()
        except Exception as e:
            logging.error(f"Error adding expense: {str(e)}")
            return False, str(e), Expense()

    def get_all_expense(self) -> list[Expense]:
        return self.expense_repository.get_all_expenses()

    def generate_expense_report(self) -> Dict:
        try:
            expenses = self.expense_repository.get_all_expenses()

            if not expenses:
                return {
                    "total_expenses": 0,
                    "max_expense": 0,
                    "min_expense": 0,
                    "most_common_category": ""
                }

            total_expenses = len(expenses)

            max_expense = max(expenses, key=lambda x: x.amount)
            min_expense = min(expenses, key=lambda x: x.amount)

            category_counts = Counter(expense.category_id for expense in expenses)
            most_common_category_id = category_counts.most_common(1)[0][0]

            common_category = self.category_repository.get_category_by_id(most_common_category_id)


            return {
                "total_expenses": total_expenses,
                "max_expense": {
                    "amount": max_expense.amount,
                    "description": max_expense.description,
                    "date": max_expense.date,
                    "category": max_expense.category.name
                },
                "min_expense": {
                    "amount": min_expense.amount,
                    "description": min_expense.description,
                    "date": min_expense.date,
                    "category": min_expense.category.name
                },
                "most_common_category_id": common_category.name
            }

        except SecurityException as e:
            logging.error(f"Security error generating expense report: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error generating expense report: {str(e)}")
            raise