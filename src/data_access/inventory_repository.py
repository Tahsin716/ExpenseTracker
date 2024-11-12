from src.data_access.data_access import DataAccess
from src.database.models.inventory_item import InventoryItem


class InventoryRepository(DataAccess):
    
    def __init__(self):
        super().__init__()

    def add_inventory_item(self, name, description, quantity, cost_price, selling_price) -> InventoryItem:
        try:
            item = InventoryItem(
                name=name,
                description=description,
                quantity=quantity,
                cost_price=cost_price,
                selling_price=selling_price
            )
            self.session.add(item)
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e

    def update_inventory_quantity(self, item_id, quantity_change) -> InventoryItem:
        try:
            item = self.session.query(InventoryItem).get(item_id)
            item.quantity += quantity_change
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e