import logging
from typing import Dict
from collections import Counter

from src.business.exception.security_exception import SecurityException
from src.data_access.category_repository import CategoryRepository
from src.data_access.expense_repository import ExpenseRepository
from src.data_access.inventory_repository import InventoryRepository
from src.data_access.sale_repository import SaleRepository


class RevenueManager:
    def __init__(self):
        self.inventory_repository = InventoryRepository()
        self.expense_repository = ExpenseRepository()
        self.category_repository = CategoryRepository()
        self.sale_repository = SaleRepository()

    def generate_expense_report(self) -> Dict:
        try:
            expenses = self.expense_repository.get_all_expenses()

            if not expenses:
                return {
                    "total_expenses": 0,
                    "max_expense": None,
                    "min_expense": None,
                    "most_common_category": None
                }

            total_expenses = len(expenses)

            max_expense = max(expenses, key=lambda x: x.amount)
            min_expense = min(expenses, key=lambda x: x.amount)

            category_counts = Counter(expense.category_id for expense in expenses)
            most_common_category_id = category_counts.most_common(1)[0][0]

            common_category = self.category_repository.get_category_by_id(most_common_category_id)


            return {
                "total_expenses": total_expenses,
                "max_expense": {
                    "amount": max_expense.amount,
                    "description": max_expense.description,
                    "date": max_expense.date,
                    "category": max_expense.category.name
                },
                "min_expense": {
                    "amount": min_expense.amount,
                    "description": min_expense.description,
                    "date": min_expense.date,
                    "category": min_expense.category.name
                },
                "most_common_category_id": common_category.name
            }

        except SecurityException as e:
            logging.error(f"Security error generating expense report: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error generating expense report: {str(e)}")
            raise

    def generate_inventory_report(self) -> Dict:
        try:
            inventory_items = self.inventory_repository.get_all_inventory_items()

            if not inventory_items:
                return {
                    "total_items": 0,
                    "max_quantity_item": None,
                    "min_quantity_item": None,
                    "max_selling_price_item": None,
                    "min_selling_price_item": None
                }

            total_items = len(inventory_items)

            max_quantity_item = max(inventory_items, key=lambda x: x.quantity)
            min_quantity_item = min(inventory_items, key=lambda x: x.quantity)

            max_selling_price_item = max(inventory_items, key=lambda x: x.selling_price)
            min_selling_price_item = min(inventory_items, key=lambda x: x.selling_price)

            return {
                "total_items": total_items,
                "max_quantity_item": {
                    "name": max_quantity_item.name,
                    "quantity": max_quantity_item.quantity,
                    "description": max_quantity_item.description,
                    "selling_price": max_quantity_item.selling_price
                },
                "min_quantity_item": {
                    "name": min_quantity_item.name,
                    "quantity": min_quantity_item.quantity,
                    "description": min_quantity_item.description,
                    "selling_price": min_quantity_item.selling_price
                },
                "max_selling_price_item": {
                    "name": max_selling_price_item.name,
                    "selling_price": max_selling_price_item.selling_price,
                    "quantity": max_selling_price_item.quantity,
                    "description": max_selling_price_item.description
                },
                "min_selling_price_item": {
                    "name": min_selling_price_item.name,
                    "selling_price": min_selling_price_item.selling_price,
                    "quantity": min_selling_price_item.quantity,
                    "description": min_selling_price_item.description
                }
            }

        except Exception as e:
            logging.error(f"Error generating inventory report: {str(e)}")
            raise

    def generate_revenue_report(self) -> Dict:
        try:
            sales = self.sale_repository.get_all_sales()
            inventory_items = self.inventory_repository.get_all_inventory_items()
            expenses = self.expense_repository.get_all_expenses()

            total_expenses = sum(expense.amount  for expense in expenses)
            total_sale_items = sum(len(sale.sale_items) for sale in sales)

            total_inventory_cost = sum(item.cost_price * item.quantity for item in inventory_items)

            total_inventory_selling_value = sum(item.selling_price * item.quantity for item in inventory_items)

            total_revenue = sum(sale.total_amount for sale in sales)

            total_cost_of_sold_items = sum(
                sum(sale_item.quantity * sale_item.item.cost_price for sale_item in sale.sale_items)
                for sale in sales
            )

            profit_from_sold_items = total_revenue - total_cost_of_sold_items
            net_profit = total_revenue - total_inventory_cost - total_expenses

            return {
                "total_inventory_cost": total_inventory_cost,
                "total_expenses": total_expenses,
                "number_of_sales": len(sales),
                "total_sale_items": total_sale_items,
                "total_inventory_selling_value": total_inventory_selling_value,
                "total_revenue": total_revenue,
                "profit_from_sold_items": profit_from_sold_items,
                "net_profit": net_profit
            }

        except Exception as e:
            logging.error(f"Error generating sales revenue report: {str(e)}")
            raise