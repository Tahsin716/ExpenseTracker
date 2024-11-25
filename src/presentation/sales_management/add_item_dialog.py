import tkinter as tk
from tkinter import ttk, messagebox
import re

from src.presentation.sales_management.search_dropdown import SearchDropdown


class AddItemDialog(tk.Toplevel):
    def __init__(self, parent, search_callback, add_callback, get_item_callback):
        super().__init__(parent)
        self.title("Add Item to Sale")
        self.geometry("400x200")

        self.search_callback = search_callback
        self.add_callback = add_callback
        self.get_item_callback = get_item_callback

        # Create item search
        ttk.Label(self, text="Search Item:").pack(pady=5)
        self.item_search = SearchDropdown(
            self,
            "Start typing item name...",
            self.search_callback
        )
        self.item_search.pack(pady=5)

        # Quantity input
        ttk.Label(self, text="Quantity:").pack(pady=5)
        self.quantity = ttk.Spinbox(self, from_=1, to=999)
        self.quantity.pack(pady=5)

        # Add button
        ttk.Button(self, text="Add to Sale", command=self.add_item).pack(pady=10)

    def parse_item_id(self, item_string : str) -> int:
        match = re.search(r'ID: (\d+)', item_string)
        return int(match.group(1)) if match else None

    def add_item(self):
        selected = self.item_search.get()

        if not selected:
            messagebox.showwarning("Warning", "Please select an item")
            self.focus()
            return

        quantity = int(self.quantity.get())
        item_id = self.parse_item_id(selected)

        item = self.get_item_callback(item_id)

        if quantity > item.quantity:
            messagebox.showerror(
                "Error",
                f"Not enough stock. Available: {item.quantity}"
            )
            self.focus()
            return

        self.add_callback(item, quantity)
        self.destroy()

    def destroy(self):
        super().destroy()
