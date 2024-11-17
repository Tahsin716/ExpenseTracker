from tkinter import ttk

from src.business.providers.security_context import SecurityContext
from src.presentation.expenses_tab import ExpensesTab
from src.presentation.user_management_tab import UserManagementTab


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.notebook = ttk.Notebook(self)

        tabs = [
            ("Users", UserManagementTab),
            ("Expenses", ExpensesTab),
            # ("Inventory", InventoryTab),
            # ("Sales", SalesTab),
            # ("Sales Tracking", SalesTrackingTab),
            # ("Reporting", ReportingTab)
        ]

        for tab_name, tab_class in tabs:
            tab = tab_class(self.notebook)
            self.notebook.add(tab, text=tab_name)

        self.notebook.pack(expand=True, fill='both')

        ttk.Button(self, text="Logout", command=self.logout).pack()

    def logout(self):
        SecurityContext.current_user = None
        self.controller.show_frame("Login")