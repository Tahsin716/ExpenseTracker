import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.utils.validation import Validation
from src.data_access.inventory_repository import InventoryRepository
from src.data_access.models.inventory_item import InventoryItem


class InventoryManager:
    def __init__(self):
        self.inventory_repository = InventoryRepository()
        self.validator = Validation()

    def create_item(self, name: str, description: str,
                 quantity: str, cost_price: str,
                 selling_price: str) -> Tuple[bool, str, InventoryItem]:
        try:
            if not name or len(name) == 0:
                raise SecurityException("Name cannot be empty")

            name = self.validator.sanitize_input(name)
            description = self.validator.sanitize_input(description)

            try:
                quantity = int(quantity)
            except ValueError:
                raise SecurityException("Quantity has to be an integer")

            try:
                cost_price = float(cost_price)
            except ValueError:
                raise SecurityException("Invalid Cost Price")

            try:
                selling_price = float(selling_price)
            except ValueError:
                raise SecurityException("Invalid Selling Price")

            if any(x < 0 for x in [quantity, cost_price, selling_price]):
                raise SecurityException("Quantity, Cost Price and Selling Price cannot be negative")

            item = self.inventory_repository.add_inventory_item(name, description, quantity, cost_price, selling_price)

            return True, "", item

        except SecurityException as e:
            logging.error(f"SecurityException adding inventory item: {str(e)}")
            return False, str(e), InventoryItem()
        except Exception as e:
            logging.error(f"Error adding inventory item: {str(e)}")
            return False, str(e), InventoryItem()

    def update_item(self, item_id: str, name : str, description : str, quantity : str, cost_price : str, selling_price : str) -> Tuple[bool, str, InventoryItem]:
        try:
            if not name or len(name) == 0:
                raise SecurityException("Name cannot be empty")

            item_id = int(item_id)
            name = self.validator.sanitize_input(name)
            description = self.validator.sanitize_input(description)

            try:
                quantity = int(quantity)
            except ValueError:
                raise SecurityException("Invalid Quantity")

            try:
                cost_price = float(cost_price)
            except ValueError:
                raise SecurityException("Invalid Cost Price")

            try:
                selling_price = float(selling_price)
            except ValueError:
                raise SecurityException("Invalid Selling Price")

            if any(x < 0 for x in [quantity, cost_price, selling_price]):
                raise SecurityException("Quantity, Cost Price and Selling Price cannot be negative")

            item = self.inventory_repository.update_inventory_item(item_id, name, description, quantity, cost_price, selling_price)

            return True, "", item

        except SecurityException as e:
            logging.error(f"SecurityException adding inventory item: {str(e)}")
            return False, str(e), InventoryItem()
        except Exception as e:
            logging.error(f"Error adding inventory item: {str(e)}")
            return False, str(e), InventoryItem()

    def get_all_inventory_items(self) -> list[InventoryItem]:
        return self.inventory_repository.get_all_inventory_items()