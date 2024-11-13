from src.data_access.data_access import DataAccess
from src.database.models.inventory_item import InventoryItem


class InventoryRepository(DataAccess):
    
    def __init__(self):
        super().__init__()

    def create(self, name, description, quantity, cost_price, selling_price) -> InventoryItem:
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

    def update(self, item_dto : InventoryItem) -> InventoryItem:
        try:
            item = self.session.query(InventoryItem).filter_by(item_id=item_dto.item_id).update({"name": item_dto.name, "description": item_dto.description,
                    "quantity": item_dto.quantity, "cost_price": item_dto.cost_price, "selling_price": item_dto.selling_price})
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e

    def update_quantity(self, item_id, quantity_change) -> InventoryItem:
        try:
            item = self.session.query(InventoryItem).get(item_id)
            item.quantity += quantity_change
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e