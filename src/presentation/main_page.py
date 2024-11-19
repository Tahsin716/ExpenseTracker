from tkinter import ttk

from src.business.providers.security_context import SecurityContext
from src.presentation.expense_management.expenses_tab import ExpensesTab
from src.presentation.inventory_management.inventory_management_tab import InventoryManagementTab
from src.presentation.user_management.user_management_tab import UserManagementTab


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.notebook = ttk.Notebook(self)

        self.tabs = {
            "Users": UserManagementTab(self.notebook),
            "Expenses": ExpensesTab(self.notebook),
            "Inventory": InventoryManagementTab(self.notebook),
            # "Sales": SalesTab(self.notebook),
            # "Sales Tracking": SalesTrackingTab(self.notebook),
            # "Reporting": ReportingTab(self.notebook)
        }

        for tab_name, tab_instance in self.tabs.items():
            self.notebook.add(tab_instance, text=tab_name)

        self.notebook.pack(expand=True, fill='both')

        ttk.Button(self, text="Logout", command=self.logout).pack()

    def logout(self):
        SecurityContext.current_user = None
        self.controller.show_frame("Login")