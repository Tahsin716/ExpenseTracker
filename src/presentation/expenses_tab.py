from tkinter import ttk

from src.business.services.expense_manager import ExpenseManager


class ExpensesTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.expense_manager = ExpenseManager()

        self.tree = ttk.Treeview(self, columns=('ID', 'Category', 'Amount', 'Description', 'Date'))
        self.tree.heading('ID', text='ID')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Date', text='Date')

        ttk.Button(self, text="Create Expense", command=self.create_expense).pack()
        self.tree.pack(expand=True, fill='both')
        self.refresh_expenses()

    def refresh_expenses(self):
        expenses = self.expense_manager.get_all_expense()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in expenses:
            self.tree.insert('', 'end', values=(expense.expense_id, expense.category.name,
                                                expense.amount, expense.description,
                                                expense.date.strftime('%Y-%m-%d')))

    def create_expense(self):
        print("Hello")