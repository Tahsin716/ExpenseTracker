import tkinter as tk
from tkinter import ttk

from src.data_access.models.sale import Sale


class SaleItemsDialog(tk.Toplevel):
    def __init__(self, parent, sale: Sale):
        super().__init__(parent)
        self.title(f"Sale Items - Sale ID: {sale.sale_id}")
        self.geometry("600x400")

        columns = ('Item ID', 'Item Name', 'Quantity', 'Price per Unit', 'Total')
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show='headings'
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for sale_item in sale.sale_items:
            self.tree.insert('', 'end', values=(
                sale_item.inventory_item_id,
                sale_item.item.name,  # Assuming InventoryItem has a name attribute
                sale_item.quantity,
                f"£{sale_item.price_per_unit:.2f}",
                f"£{sale_item.quantity * sale_item.price_per_unit:.2f}"
            ))

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        close_button.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)