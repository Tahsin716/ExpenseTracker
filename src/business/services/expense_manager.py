import logging
from datetime import datetime
from typing import Optional, Dict

from src.business.exception.security_exception import SecurityException
from src.business.providers.security_context import SecurityContext
from src.business.utils.validation import Validation
from src.data_access.expense_repository import ExpenseRepository


class ExpenseManager:

    def __init__(self):
        self.expense_repository = ExpenseRepository()
        self.validator = Validation()

    def add_expense(self, category_id: str, amount: float,
                    description: str, date: Optional[datetime] = None) -> bool:
        try:
            description = self.validator.sanitize_input(description)

            if SecurityContext.current_user is None:
                raise SecurityException("Invalid user")

            if not isinstance(amount, (int, float)) or amount <= 0:
                raise SecurityException("Invalid amount")

            return self.expense_repository.add_expense(
                SecurityContext.current_user.user_id,
                category_id,
                amount,
                description,
                date or datetime.now()
            )

        except SecurityException as e:
            logging.error(f"Security error adding expense: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error adding expense: {str(e)}")
            raise

    def get_expense_summary(self, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict:
        try:
            if SecurityContext.current_user is None:
                raise SecurityException("Invalid user")

            return self.expense_repository.get_user_expenses(
                SecurityContext.current_user.user_id,
                start_date,
                end_date
            )

        except SecurityException as e:
            logging.error(f"Security error getting expense summary: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error getting expense summary: {str(e)}")
            raise