from src.data_access.data_access import DataAccess
from src.data_access.inventory_repository import InventoryRepository
from src.data_access.models.inventory_item import InventoryItem
from src.data_access.models.sale import Sale
from src.data_access.models.sale_item import SaleItem


class SaleRepository(DataAccess):

    def __init__(self):
        super().__init__()
        self.inventory_repository = InventoryRepository()

    def create_sale(self, user_id : str, items: list[InventoryItem]) -> Sale:
        try:
            total_amount = sum(item['quantity'] * item['price_per_unit'] for item in items)
            sale = Sale(user_id=user_id, total_amount=total_amount)
            self.session.add(sale)
            self.session.flush()

            for item in items:
                sale_item = SaleItem(
                    sale_id=sale.sale_id,
                    item_id=item['item_id'],
                    quantity=item['quantity'],
                    price_per_unit=item['price_per_unit']
                )
                self.session.add(sale_item)
                self.inventory_repository.update_quantity(item['item_id'], -item['quantity'])

            self.session.commit()
            return sale
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_sales(self) -> list[Sale]:
        return self.session.query(Sale).all()
