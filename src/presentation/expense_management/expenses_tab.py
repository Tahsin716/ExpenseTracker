from tkinter import ttk

from src.business.services.expense_manager import ExpenseManager
from src.presentation.expense_management.create_category_form import CreateCategoryForm
from src.presentation.expense_management.create_expense_form import CreateExpenseForm


class ExpensesTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.expense_manager = ExpenseManager()

        self.action_frame = ttk.Frame(self)

        self.tree = ttk.Treeview(self, columns=('ID', 'Category', 'Amount', 'Description', 'Date'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Date', text='Date')

        self.create_button = ttk.Button(self.action_frame, text="Create Expense", command=self.create_expense)
        self.create_button.pack(side='left', padx=5)

        self.create_category = ttk.Button(self.action_frame, text="Create Category", command=self.create_category)
        self.create_category.pack(side='left', padx=5)

        self.action_frame.pack(fill='x', pady=5)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_data()

    def refresh_data(self):
        expenses = self.expense_manager.get_all_expense()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in expenses:
            self.tree.insert('', 'end', values=(expense.expense_id, expense.category.name,
                                                expense.amount, expense.description,
                                                expense.date.strftime('%Y-%m-%d')))

    def create_expense(self):
        CreateExpenseForm(self, self.refresh_data)

    def create_category(self):
        CreateCategoryForm(self)