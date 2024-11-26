from src.data_access.data_access import DataAccess
from src.data_access.inventory_repository import InventoryRepository
from src.data_access.models.customer import Customer
from src.data_access.models.inventory_item import InventoryItem
from src.data_access.models.sale import Sale
from src.data_access.models.sale_item import SaleItem


class SaleRepository(DataAccess):

    def __init__(self):
        super().__init__()
        self.inventory_repository = InventoryRepository()

    def create_sale(self, customer : Customer, items: list[InventoryItem]) -> Sale:
        try:
            total_amount = sum(item.quantity * item.selling_price for item in items)
            sale = Sale(customer_id=customer.customer_id, total_amount=total_amount)
            self.session.add(sale)
            self.session.flush()

            for item in items:
                sale_item = SaleItem(
                    sale_id=sale.sale_id,
                    inventory_item_id=item.item_id,
                    quantity=item.quantity,
                    price_per_unit=item.selling_price
                )
                self.session.add(sale_item)

            self.session.commit()
            return self.session.query(Sale).filter_by(sale_id=sale.sale_id).first()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_sales(self) -> list[Sale]:
        return self.session.query(Sale).all()
