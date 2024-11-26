

from src.data_access.data_access import DataAccess
from src.data_access.models.inventory_item import InventoryItem


class InventoryRepository(DataAccess):
    
    def __init__(self):
        super().__init__()

    def add_inventory_item(self, name : str, description : str, quantity : int, cost_price: float, selling_price : float) -> InventoryItem:
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

    def update_inventory_item(self, item_id: int, name : str, description : str, quantity : int, cost_price : float, selling_price : float) -> InventoryItem:
        try:
            item = self.session.query(InventoryItem).filter_by(item_id=item_id).update({"name": name, "description": description,
                    "quantity": quantity, "cost_price": cost_price, "selling_price": selling_price})
            self.session.commit()
            return item
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_item(self, item_id: int) :
        try:
            self.session.query(InventoryItem).filter_by(item_id=item_id).delete(synchronize_session=False)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_inventory_items(self) -> list[InventoryItem]:
        return self.session.query(InventoryItem).all()

    def get_item_by_id(self, item_id : int) -> InventoryItem:
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

    def search_items_by_name(self, search_text):
        self.session.expire_all()
        return self.session.query(InventoryItem).filter(
            InventoryItem.name.ilike(f"%{search_text}%")
        ).all()