from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models.base import Base
from src.database.models.expense import Expense
from src.database.models.inventory_item import InventoryItem
from src.database.models.sale import Sale
from src.database.models.sale_item import SaleItem
from src.database.models.user import User


class DataAccess:
    def __init__(self, connection_string="sqlite:////database/db/expense_tracker.db"):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # User Management
    def create_user(self, username, password, email):
        try:
            user = User(
                username=username,
                password_hash=password, # TODO: Hash the password later
                email=email
            )
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    # Expense Management
    def add_expense(self, user_id, category_id, amount, description, date):
        try:
            expense = Expense(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                description=description,
                date=date
            )
            self.session.add(expense)
            self.session.commit()
            return expense
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_expenses(self, user_id, start_date=None, end_date=None):
        query = self.session.query(Expense).filter_by(user_id=user_id)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        return query.all()

    # Inventory Management
    def add_inventory_item(self, name, description, quantity, cost_price, selling_price):
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

    def update_inventory_quantity(self, item_id, quantity_change):
        try:
            item = self.session.query(InventoryItem).get(item_id)
            if item:
                item.quantity += quantity_change
                self.session.commit()
                return item
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    # Sales Management
    def create_sale(self, user_id, items):
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
                self.update_inventory_quantity(item['item_id'], -item['quantity'])

            self.session.commit()
            return sale
        except Exception as e:
            self.session.rollback()
            raise e