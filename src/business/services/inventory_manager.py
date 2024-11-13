import logging

from src.business.exception.security_exception import SecurityException
from src.business.utils.validation import Validation
from src.data_access.inventory_repository import InventoryRepository
from src.database.models.inventory_item import InventoryItem


class InventoryManagement:
    def __init__(self):
        self.inventory_repository = InventoryRepository()
        self.validator = Validation()

    def create_item(self, name: str, description: str,
                 quantity: int, cost_price: float,
                 selling_price: float) -> InventoryItem:
        try:
            name = self.validator.sanitize_input(name)
            description = self.validator.sanitize_input(description)

            if not all(isinstance(x, (int, float)) for x in
                       [quantity, cost_price, selling_price]):
                raise SecurityException("Invalid numeric values")

            if any(x < 0 for x in [quantity, cost_price, selling_price]):
                raise SecurityException("Values cannot be negative")

            return self.inventory_repository.create(
                name, description, quantity, cost_price, selling_price)

        except SecurityException as e:
            logging.error(f"SecurityException adding inventory item: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error adding inventory item: {str(e)}")
            raise

    def update_item(self, item_dto : InventoryItem) -> InventoryItem:
        item_dto.name = self.validator.sanitize_input(item_dto.name)
        item_dto.description = self.validator.sanitize_input(item_dto.description)

        if not all(isinstance(x, (int, float)) for x in
                   [item_dto.quantity, item_dto.cost_price, item_dto.selling_price]):
            raise SecurityException("Invalid numeric values")

        if any(x < 0 for x in [item_dto.quantity, item_dto.cost_price, item_dto.
                selling_price]):
            raise SecurityException("Values cannot be negative")

        return self.inventory_repository.update(item_dto)