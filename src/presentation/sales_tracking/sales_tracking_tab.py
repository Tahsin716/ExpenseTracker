from tkinter import ttk

from src.business.providers.security_context import SecurityContext
from src.business.services.sale_manager import SaleManager


class SalesTrackingTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.sale_manager = SaleManager()
        self.access_message = ttk.Label(self, text="Access Denied! Admin only Access")
        self.tree = ttk.Treeview(self, columns=('ID', 'Date', 'Customer Phone Number', 'Total'), show="headings")
        self.display()


    def display(self):
        if SecurityContext.current_user is None or SecurityContext.current_user.role != 'admin':
            self.access_message.pack()
            self.tree.pack_forget()
            return
        else:
            self.access_message.pack_forget()

        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Customer Phone Number', text='Customer Phone Number')
        self.tree.heading('Total', text='Total')

        self.tree.column('ID', width=50)
        self.tree.column('Date', width=200)
        self.tree.column('Customer Phone Number', width=100)
        self.tree.column('Total', width=100)

        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        self.refresh_data()

    def refresh_data(self):
        sales = self.sale_manager.get_all_sales()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for sale in sales:
            self.tree.insert('', 'end', values=(sale.sale_id, sale.sale_date.strftime('%Y-%m-%d'),
                                                sale.customer.phone_number, sale.total_amount))
