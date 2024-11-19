import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.expense_manager import ExpenseManager


class CreateExpenseForm(tk.Toplevel):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)
        self.refresh_callback = refresh_callback
        self.expense_manager = ExpenseManager()
        #self.category_manager = CategoryManager()

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
        ttk.Button(self, text="Cancel", command=self.destroy).grid(row=4, column=1, padx=10, pady=10)

    def load_categories(self):
        pass

    def save_expense(self):
        pass
