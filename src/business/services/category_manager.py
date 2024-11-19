import logging

from typing_extensions import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.utils.validation import Validation
from src.data_access.category_repository import CategoryRepository
from src.data_access.models.category import Category


class CategoryManager:

    def __init__(self):
        self.category_repository = CategoryRepository()
        self.validator = Validation()

    def add_category(self, name : str, description : str) -> Tuple[bool, str, Category]:
        try:
            if not name or len(name) == 0:
                raise SecurityException("name cannot be empty")

            if not description or len(description) == 0:
                raise SecurityException("description cannot be empty")

            exists = self.get_category_by_name(name)

            if exists:
                raise SecurityException("Category with the given name already exists")

            category = self.category_repository.add_category(name, description)
            return True, "", category

        except SecurityException as e:
            logging.error(f"Security exception while adding category: {str(e)}")
            return False, str(e), Category()
        except Exception as e:
            logging.error(f"Exception while adding category: {str(e)}")
            return False, str(e), Category()

    def get_all_categories(self) -> list[Category]:
        return self.category_repository.get_all_categories()

    def get_category_by_name(self, name : str) -> Category:
        return self.category_repository.get_category_by_name(name)