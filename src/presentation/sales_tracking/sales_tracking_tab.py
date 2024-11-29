from tkinter import ttk, font, messagebox
import tkinter as tk
from src.business.providers.security_context import SecurityContext
from src.business.services.sale_manager import SaleManager
from src.presentation.sales_tracking.sale_items_dialog import SaleItemsDialog


class SalesTrackingTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.sale_manager = SaleManager()
        self.access_message = ttk.Label(self, text="Access Denied! Admin only Access")

        self.action_frame = ttk.Frame(self)
        self.view_sale_items_button = ttk.Button(self.action_frame, text="View Sale Items",
                                                command=self.view_sale_items)

        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'Date', 'Customer Phone Number', 'Total'),
            show="headings",
        )
        self.sales_dict = {}

        self.display()

    def display(self):
        if SecurityContext.current_user is None or SecurityContext.current_user.role != 'admin':
            self.access_message.pack()
            self.tree.pack_forget()
            self.view_sale_items_button.pack_forget()
            self.action_frame.pack_forget()
            return
        else:
            self.access_message.pack_forget()

        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Customer Phone Number', text='Customer Phone Number')
        self.tree.heading('Total', text='Total')

        self.tree.column('ID', width=50)
        self.tree.column('Date', width=200)
        self.tree.column('Customer Phone Number', width=150)
        self.tree.column('Total', width=100)

        self.view_sale_items_button.pack(side='left', padx=5)
        self.action_frame.pack(fill='x', pady=5)
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)

        self.refresh_data()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.sales_dict.clear()

        sales = self.sale_manager.get_all_sales()

        for sale in sales:
            self.sales_dict[sale.sale_id] = sale

            self.tree.insert('', 'end', values=(
                sale.sale_id,
                sale.sale_date.strftime('%Y-%m-%d'),
                sale.customer.phone_number,
                f"£{sale.total_amount:.2f}",
            ))

    def view_sale_items(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a sale to view its items.")
            return

        sale_id = self.tree.item(selected_item[0])['values'][0]
        sale = self.sales_dict.get(sale_id)

        if sale:
            SaleItemsDialog(self, sale)
