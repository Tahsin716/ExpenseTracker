from datetime import datetime, timezone

from sqlalchemy import select

from src.business.providers.roles import Roles
from src.business.providers.security_context import SecurityContext
from src.business.utils.password_manager import PasswordManager
from src.data_access.data_access import DataAccess
from src.data_access.models.category import Category
from src.data_access.models.customer import Customer
from src.data_access.models.expense import Expense
from src.data_access.models.inventory_item import InventoryItem
from src.data_access.models.sale import Sale
from src.data_access.models.sale_item import SaleItem
from src.data_access.models.user import User


class SeedData(DataAccess):

    def __init__(self):
        super().__init__()

    def seed_data(self):
        try:
            self.category_seed()
            self.customer_seed()
            self.inventory_seed()
            self.user_seed()
            self.sale_seed()
            self.sale_item_seed()
            self.expense_seed()
            self.session.commit()
            print("Seeding completed successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"An error occurred during seeding: {e}")
        finally:
            self.session.close()

    def expense_seed(self):
        expenses = [
            Expense(
                category_id=1,  # Replace with actual Category IDs
                amount=300.0,
                description="Purchased office supplies",
                date=datetime(2024, 11, 2, tzinfo=timezone.utc)
            ),
            Expense(
                category_id=2,
                amount=500.0,
                description="Travel expenses for conference",
                date=datetime(2024, 11, 6, tzinfo=timezone.utc)
            )
        ]
        for expense in expenses:
            exists = self.session.execute(
                select(Expense).where(
                    (Expense.category_id == expense.category_id) &
                    (Expense.date == expense.date)
                )
            ).scalar_one_or_none()
            if not exists:
                self.session.add(expense)

    def sale_item_seed(self):
        sale_items = [
            SaleItem(
                sale_id=1,
                inventory_item_id=1,
                quantity=2,
                price_per_unit=700.0
            ),
            SaleItem(
                sale_id=2,
                inventory_item_id=2,
                quantity=1,
                price_per_unit=100.0
            )
        ]
        for sale_item in sale_items:
            exists = self.session.execute(
                select(SaleItem).where(
                    (SaleItem.sale_id == sale_item.sale_id) &
                    (SaleItem.inventory_item_id == sale_item.inventory_item_id)
                )
            ).scalar_one_or_none()
            if not exists:
                self.session.add(sale_item)

    def sale_seed(self):
        sales = [
            Sale(
                total_amount=1500.0,
                sale_date=datetime(2024, 11, 1, tzinfo=timezone.utc),
                customer_id=1
            ),
            Sale(
                total_amount=2000.0,
                sale_date=datetime(2024, 11, 5, tzinfo=timezone.utc),
                customer_id=2
            )
        ]
        for sale in sales:
            exists = self.session.execute(
                select(Sale).where(Sale.sale_date == sale.sale_date)
            ).scalar_one_or_none()
            if not exists:
                self.session.add(sale)

    def user_seed(self):
        users = [
            User(first_name="John", last_name="Doe",
                 password_hash=PasswordManager.hash_password(SecurityContext.default_password),
                 email="john.doe@example.com", role=Roles.ADMIN),
            User(first_name="Jane", last_name="Smith",
                 password_hash=PasswordManager.hash_password(SecurityContext.default_password),
                 email="jane.smith@example.com", role=Roles.USER)
        ]
        for user in users:
            exists = self.session.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
            if not exists:
                self.session.add(user)

    def inventory_seed(self):
        inventory_items = [
            InventoryItem(name="Laptop", description="Dell Laptop", quantity=10, cost_price=500, selling_price=700),
            InventoryItem(name="Chair", description="Office Chair", quantity=15, cost_price=50, selling_price=100),
        ]
        for item in inventory_items:
            exists = self.session.execute(select(InventoryItem).where(InventoryItem.name == item.name)).scalar_one_or_none()
            if not exists:
                self.session.add(item)

    def customer_seed(self):
        customers = [
            Customer(phone_number="1234567890"),
            Customer(phone_number="0987654321")
        ]
        for customer in customers:
            exists = self.session.execute(
                select(Customer).where(Customer.phone_number == customer.phone_number)
            ).scalar_one_or_none()
            if not exists:
                self.session.add(customer)

    def category_seed(self):
        categories = [
            Category(name="Office Supplies", description="Expenses related to office supplies"),
            Category(name="Travel", description="Travel-related expenses")
        ]
        for category in categories:
            exists = self.session.execute(select(Category).where(Category.name == category.name)).scalar_one_or_none()
            if not exists:
                self.session.add(category)
