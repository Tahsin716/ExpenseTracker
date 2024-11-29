import tkinter as tk
from tkinter import ttk
from typing import Dict

class InventoryReportDialog(tk.Toplevel):
    def __init__(self, parent, report_data: Dict):
        super().__init__(parent)
        self.title("Inventory Report")
        self.geometry("500x600")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Inventory Report", style='Title.TLabel').pack(pady=(0,10))
        ttk.Label(main_frame, text=f"Total Items: {report_data['total_items']}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Item with Maximum Quantity", style='Title.TLabel').pack(anchor='w')
        max_qty_item = report_data['max_quantity_item']
        ttk.Label(main_frame, text=f"Name: {max_qty_item['name']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Quantity: {max_qty_item['quantity']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Description: {max_qty_item['description']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Selling Price: ${max_qty_item['selling_price']:.2f}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Item with Minimum Quantity", style='Title.TLabel').pack(anchor='w')
        min_qty_item = report_data['min_quantity_item']
        ttk.Label(main_frame, text=f"Name: {min_qty_item['name']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Quantity: {min_qty_item['quantity']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Description: {min_qty_item['description']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Selling Price: ${min_qty_item['selling_price']:.2f}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Item with Maximum Selling Price", style='Title.TLabel').pack(anchor='w')
        max_price_item = report_data['max_selling_price_item']
        ttk.Label(main_frame, text=f"Name: {max_price_item['name']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Selling Price: ${max_price_item['selling_price']:.2f}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Quantity: {max_price_item['quantity']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Description: {max_price_item['description']}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Item with Minimum Selling Price", style='Title.TLabel').pack(anchor='w')
        min_price_item = report_data['min_selling_price_item']
        ttk.Label(main_frame, text=f"Name: {min_price_item['name']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Selling Price: ${min_price_item['selling_price']:.2f}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Quantity: {min_price_item['quantity']}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Description: {min_price_item['description']}", style='TLabel').pack(anchor='w')

        close_button = ttk.Button(main_frame, text="Close", command=self.destroy)
        close_button.pack(pady=20)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)