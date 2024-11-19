import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.inventory_manager import InventoryManager


class CreateInventoryForm(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.inventory_manager = InventoryManager()
        self.callback = callback

        self.title("Create Inventory Item")
        self.geometry("400x300")

        self.name = tk.StringVar()
        self.description = tk.StringVar()
        self.quantity = tk.StringVar()
        self.cost_price = tk.StringVar()
        self.selling_price = tk.StringVar()

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(self, textvariable=self.name)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.description)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Quantity:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.quantity)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Cost Price:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.cost_price)
        self.description_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self, text="Selling Price:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self, textvariable=self.selling_price)
        self.description_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(self, text="Save", command=self.save_inventory).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=5, column=1, padx=10, pady=10)

    def save_inventory(self):
        name = self.name.get()
        description = self.description.get()
        quantity = self.quantity.get()
        cost_price = self.cost_price.get()
        selling_price = self.selling_price.get()

        success, message, item = self.inventory_manager.create_item(name, description, quantity, cost_price, selling_price)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "Successfully created new inventory item")
            self.callback()
            self.close_form()


    def close_form(self):
        self.destroy()