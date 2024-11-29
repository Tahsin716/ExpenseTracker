from tkinter import ttk

from src.business.providers.security_context import SecurityContext
from src.business.services.expense_manager import ExpenseManager
from src.presentation.report_management.expense_report_dialog import ExpenseReportDialog


class ReportingTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.expense_manager = ExpenseManager()

        self.access_message = ttk.Label(self, text="Access Denied! Admin only Access")
        self.action_frame = ttk.Frame(self)
        self.expense_report_button = ttk.Button(self.action_frame, text="Generate Expense Report", command=self.generate_expense_report)
        self.inventory_report_button = ttk.Button(self.action_frame, text="Generate Inventory Report", command=self.generate_inventory_report)
        self.revenue_report_button = ttk.Button(self.action_frame, text="Generate Revenue Report", command=self.generate_revenue_report())

        self.display()


    def display(self):
        if SecurityContext.current_user is None or SecurityContext.current_user.role != 'admin':
            self.access_message.pack()
            self.expense_report_button.pack_forget()
            self.inventory_report_button.pack_forget()
            self.revenue_report_button.pack_forget()
            self.action_frame.pack_forget()
        else:
            self.access_message.pack_forget()
            self.expense_report_button.pack(side='left', padx=5)
            self.inventory_report_button.pack(side='left', padx=5)
            self.revenue_report_button.pack(side='left', padx=5)
            self.action_frame.pack(fill='x', pady=5)


    def generate_expense_report(self):
        report_data = self.expense_manager.generate_expense_report()
        ExpenseReportDialog(self, report_data)

    def generate_inventory_report(self):
        # Generate inventory report logic
        pass

    def generate_revenue_report(self):
        pass