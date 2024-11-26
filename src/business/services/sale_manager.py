import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.data_access.inventory_repository import InventoryRepository
from src.data_access.models.customer import Customer
from src.data_access.models.inventory_item import InventoryItem
from src.data_access.models.sale import Sale
from src.data_access.sale_repository import SaleRepository


class SaleManager:
    def __init__(self):
        self.sales_repository = SaleRepository()
        self.inventory_repository = InventoryRepository()

    def create_sale(self, customer : Customer, items : list[InventoryItem]) -> Tuple[bool, str, Sale]:
        try:
            if not Customer:
                raise SecurityException("Customer cannot be empty")

            if not items or items.count == 0:
                raise SecurityException("Items cannot be empty")

            all_inventory_items = all(isinstance(item, InventoryItem) for item in items)

            if not all_inventory_items:
                raise SecurityException("Some objects are not instance of InventoryItem")

            sale = self.sales_repository.create_sale(customer, items)

            for item in items:
                self.inventory_repository.update_quantity(item.item_id, -item.quantity)

            return True, "", sale
        except SecurityException as e:
            logging.error(f"SecurityException occurred: {str(e)}")
            return False, str(e), Sale()
        except Exception as e:
            logging.error(f"Error occurred while saving sale: {str(e)}")
            return False, str(e), Sale()

