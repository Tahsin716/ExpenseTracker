import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.category_manager import CategoryManager
from src.business.services.expense_manager import ExpenseManager


class CreateExpenseForm(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.expense_manager = ExpenseManager()
        self.category_manager = CategoryManager()

        self.title("Create Expense")
        self.geometry("400x300")

        self.category_name = tk.StringVar()
        self.amount = tk.StringVar()
        self.description = tk.StringVar()
        self.date = tk.StringVar()

        ttk.Label(self, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_name, state="readonly")
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.load_categories()

        ttk.Label(self, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(self, textvariable=self.amount)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.description)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ttk.Entry(self, textvariable=self.date)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self, text="Save", command=self.save_expense).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=4, column=1, padx=10, pady=10)

    def load_categories(self):
        categories = self.category_manager.get_all_categories()
        self.category_dropdown["values"] = [category.name for category in categories]

    def save_expense(self):
        category_name = self.category_name.get()
        amount = self.amount.get()
        description = self.description.get()
        date = self.date.get()

        category = self.category_manager.get_category_by_name(category_name)

        if not category:
            messagebox.showerror("Error", "Category name cannot be empty")
            self.focus()
            return

        success, message, expense = self.expense_manager.add_expense(category.category_id, amount, description, date)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Successfully added new expense")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()
