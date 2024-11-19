import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.category_manager import CategoryManager


class CreateCategoryForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.category_manager = CategoryManager()

        self.title("Create Category")
        self.geometry("400x300")

        self.category_name = tk.StringVar()
        self.category_description = tk.StringVar()

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(self, textvariable=self.category_name)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.category_description)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self, text="Save", command=self.save_category).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=4, column=1, padx=10, pady=10)

    def save_category(self):
        category_name = self.category_name.get()
        description = self.category_description.get()

        success, message, expense = self.category_manager.add_category(category_name, description)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Successfully added new expense")
            self.close_form()

    def close_form(self):
        self.destroy()
