import logging

from src.data_access.data_access import DataAccess
from src.data_access.models.inventory_item import InventoryItem


class InventoryRepository(DataAccess):
    
    def __init__(self):
        super().__init__()

    def create(self, name : str, description : str, quantity : int, cost_price: float, selling_price : float) -> InventoryItem:
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

    def delete(self, item_id: str) -> bool:
        item = self.session.query(InventoryItem).filter_by(item_id=item_id).first()

        if item is None:
            logging.log("No InventoryItem found with the given item_id")
            return False

        try:
            self.session.query(InventoryItem).filter_by(item_id).delete(synchronize_session=False)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def get_inventory_items(self) -> list[InventoryItem]:
        return self.session.query(InventoryItem).all()

    def get_item_by_id(self, item_id : str) -> InventoryItem:
        return self.session.query(InventoryItem).filter_by(item_id=item_id).first()

    def update_quantity(self, item_id : str, quantity_change : int) -> InventoryItem:
        try:
            item = self.session.query(InventoryItem).get(item_id)
            item.quantity += quantity_change
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e