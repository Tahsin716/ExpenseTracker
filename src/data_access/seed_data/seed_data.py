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
                category_id=1,
                amount=300.0,
                description="Rent for last month",
                date=datetime(2024, 11, 2, tzinfo=timezone.utc)
            ),
            Expense(
                category_id=2,
                amount=500.0,
                description="Utility bill for last month",
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
                price_per_unit=35.0  # Espresso Beans
            ),
            SaleItem(
                sale_id=2,
                inventory_item_id=2,
                quantity=1,
                price_per_unit=2.0  # Milk
            ),
            SaleItem(
                sale_id=3,
                inventory_item_id=5,
                quantity=5,
                price_per_unit=3.50  # Pastries
            ),
            SaleItem(
                sale_id=4,
                inventory_item_id=6,
                quantity=10,
                price_per_unit=1.50  # Tea Bags
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
                total_amount=70.0,  # 2*35.0
                sale_date=datetime(2024, 11, 1, tzinfo=timezone.utc),
                customer_id=1
            ),
            Sale(
                total_amount=2.0,  # 1*2.0
                sale_date=datetime(2024, 11, 5, tzinfo=timezone.utc),
                customer_id=2
            ),
            Sale(
                total_amount=17.50,  # 5*3.50
                sale_date=datetime(2024, 11, 10, tzinfo=timezone.utc),
                customer_id=3
            ),
            Sale(
                total_amount=15.0,  # 10*1.50
                sale_date=datetime(2024, 11, 15, tzinfo=timezone.utc),
                customer_id=4
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
                 email="jane.smith@example.com", role=Roles.USER),
            User(first_name="Alice", last_name="Johnson",
                 password_hash=PasswordManager.hash_password(SecurityContext.default_password),
                 email="alice.johnson@example.com", role=Roles.USER),
            User(first_name="Bob", last_name="Brown",
                 password_hash=PasswordManager.hash_password(SecurityContext.default_password),
                 email="bob.brown@example.com", role=Roles.USER),
            User(first_name="Charlie", last_name="Davis",
                 password_hash=PasswordManager.hash_password(SecurityContext.default_password),
                 email="charlie.davis@example.com", role=Roles.ADMIN)
        ]

        for user in users:
            exists = self.session.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
            if not exists:
                self.session.add(user)

    def inventory_seed(self):
        inventory_items = [
            InventoryItem(name="Espresso Beans", description="High-quality espresso beans", quantity=50, cost_price=20, selling_price=35),
            InventoryItem(name="Milk", description="Fresh whole milk", quantity=200, cost_price=1, selling_price=2),
            InventoryItem(name="Sugar", description="Refined sugar packets", quantity=500, cost_price=0.10, selling_price=0.50),
            InventoryItem(name="Coffee Cups", description="12 oz coffee cups", quantity=1000, cost_price=0.20, selling_price=1),
            InventoryItem(name="Pastries", description="Assorted fresh pastries", quantity=100, cost_price=1.50, selling_price=3.50),
            InventoryItem(name="Tea Bags", description="Various tea blends", quantity=300, cost_price=0.25, selling_price=1.50)
        ]

        for item in inventory_items:
            exists = self.session.execute(select(InventoryItem).where(InventoryItem.name == item.name)).scalar_one_or_none()
            if not exists:
                self.session.add(item)

    def customer_seed(self):
        customers = [
            Customer(phone_number="+447912345678"),
            Customer(phone_number="+447876543210"),
            Customer(phone_number="+447911112222"),
            Customer(phone_number="+447812345678"),
            Customer(phone_number="+447833333444")
        ]

        for customer in customers:
            exists = self.session.execute(
                select(Customer).where(Customer.phone_number == customer.phone_number)
            ).scalar_one_or_none()
            if not exists:
                self.session.add(customer)

    def category_seed(self):
        categories = [
            Category(name="Rent", description="Monthly rent for the coffee shop premises"),
            Category(name="Utilities", description="Expenses for electricity, water, and other utilities"),
            Category(name="Payroll", description="Salaries and wages for employees"),
            Category(name="Supplies", description="Coffee beans, cups, and other necessary supplies"),
            Category(name="Equipment Maintenance", description="Costs for maintaining and repairing equipment"),
            Category(name="Marketing", description="Advertising and promotional expenses")
        ]

        for category in categories:
            exists = self.session.execute(select(Category).where(Category.name == category.name)).scalar_one_or_none()
            if not exists:
                self.session.add(category)
