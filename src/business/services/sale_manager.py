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

    def create_sale(self, customer : Customer, sale_items : dict ) -> Tuple[bool, str, Sale]:
        try:
            if not Customer:
                raise SecurityException("Customer cannot be empty")

            if not sale_items:
                raise SecurityException("Items cannot be empty")

            sale = self.sales_repository.create_sale(customer, sale_items)

            for sale_item in sale_items.values():
                self.inventory_repository.update_quantity(sale_item['item_id'], -sale_item['quantity'])

            return True, "", sale
        except SecurityException as e:
            logging.error(f"SecurityException occurred: {str(e)}")
            return False, str(e), Sale()
        except Exception as e:
            logging.error(f"Error occurred while saving sale: {str(e)}")
            return False, str(e), Sale()

    def get_all_sales(self) -> list[Sale]:
        return self.sales_repository.get_all_sales()

