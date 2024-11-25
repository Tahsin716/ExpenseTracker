from tkinter import ttk

from src.business.services.user_manager import UserManager
from src.presentation.sales_management.search_dropdown import SearchDropdown


class SalesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_manager = UserManager()

        # Customer search section
        customer_frame = ttk.LabelFrame(self, text="Customer Information")
        customer_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(customer_frame, text="Phone Number:").pack(side='left', padx=5)
        self.customer_search = SearchDropdown(
            customer_frame,
            "Enter phone number...",
            self.search_customers
        )
        self.customer_search.pack(side='left', padx=5)

        # Create treeview for selected items
        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
            show='headings'
        )
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Total', text='Total')

        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=200)
        self.tree.column('Quantity', width=100)
        self.tree.column('Price', width=100)
        self.tree.column('Total', width=100)

        self.tree.pack(expand=True, fill='both', padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)

        # ttk.Button(
        #     button_frame,
        #     text="Add Item",
        #     command=self.show_add_item_dialog
        # ).pack(side='left', padx=5)
        #
        # ttk.Button(
        #     button_frame,
        #     text="Remove Selected",
        #     command=self.remove_selected_item
        # ).pack(side='left', padx=5)

        # Total and complete sale frame
        total_frame = ttk.Frame(self)
        total_frame.pack(fill='x', padx=5, pady=5)

        self.total_label = ttk.Label(
            total_frame,
            text="Total: $0.00",
            font=('TkDefaultFont', 12, 'bold')
        )
        self.total_label.pack(side='left', padx=5)

        # ttk.Button(
        #     total_frame,
        #     text="Complete Sale",
        #     command=self.complete_sale
        # ).pack(side='right', padx=5)

        # Initialize sale items dictionary
        self.sale_items = {}

    def search_customers(self, phone_number):
        customers = self.user_manager.search_customer_by_phone_number(phone_number)
        return [customer.phone_number for customer in customers]

    # def show_add_item_dialog(self):
    #     AddItemDialog(self, self.search_items, self.add_item)

    # def add_item(self, item, quantity):
    #     item_id = item.item_id
    #
    #     if item_id in self.sale_items:
    #         # Merge quantities if item already exists
    #         existing_qty = self.sale_items[item_id]['quantity']
    #         new_qty = existing_qty + quantity
    #
    #         if new_qty > item.quantity:
    #             messagebox.showerror(
    #                 "Error",
    #                 f"Not enough stock. Available: {item.quantity}"
    #             )
    #             return
    #
    #         self.sale_items[item_id]['quantity'] = new_qty
    #         self.sale_items[item_id]['total'] = new_qty * item.selling_price
    #
    #         # Update existing tree item
    #         for child in self.tree.get_children():
    #             if self.tree.item(child)['values'][0] == item_id:
    #                 self.tree.item(
    #                     child,
    #                     values=(
    #                         item_id,
    #                         item.name,
    #                         new_qty,
    #                         f"${item.selling_price:.2f}",
    #                         f"${new_qty * item.selling_price:.2f}"
    #                     )
    #                 )
    #                 break
    #     else:
    #         # Add new item
    #         self.sale_items[item_id] = {
    #             'item': item,
    #             'quantity': quantity,
    #             'total': quantity * item.selling_price
    #         }
    #
    #         self.tree.insert(
    #             '',
    #             'end',
    #             values=(
    #                 item_id,
    #                 item.name,
    #                 quantity,
    #                 f"${item.selling_price:.2f}",
    #                 f"${quantity * item.selling_price:.2f}"
    #             )
    #         )
    #
    #     self.update_total()
    #
    # def remove_selected_item(self):
    #     selected = self.tree.selection()
    #     if not selected:
    #         return
    #
    #     item_id = self.tree.item(selected[0])['values'][0]
    #     del self.sale_items[item_id]
    #     self.tree.delete(selected[0])
    #     self.update_total()
    #
    # def update_total(self):
    #     total = sum(item['total'] for item in self.sale_items.values())
    #     self.total_label.configure(text=f"Total: ${total:.2f}")
    #
    # def complete_sale(self):
    #     if not self.sale_items:
    #         messagebox.showwarning("Warning", "No items in sale")
    #         return
    #
    #     phone_number = self.customer_search.get()
    #
    #     # Create or get customer
    #     if phone_number:
    #         customer = self.session.query(Customer).filter_by(
    #             phone_number=phone_number
    #         ).first()
    #
    #         if not customer:
    #             customer = Customer(phone_number=phone_number)
    #             self.session.add(customer)
    #
    #     try:
    #         # Create sale
    #         total_amount = sum(item['total'] for item in self.sale_items.values())
    #
    #         sale = Sale(
    #             total_amount=total_amount,
    #             customer_phone_number=phone_number if phone_number else None
    #         )
    #         self.session.add(sale)
    #
    #         # Add sale items and update inventory
    #         for item_id, sale_item in self.sale_items.items():
    #             item = sale_item['item']
    #             quantity = sale_item['quantity']
    #
    #             # Create sale item
    #             new_sale_item = SaleItem(
    #                 sale=sale,
    #                 inventory_item_id=item_id,
    #                 quantity=quantity,
    #                 price_per_unit=item.selling_price
    #             )
    #             self.session.add(new_sale_item)
    #
    #             # Update inventory quantity
    #             item.quantity -= quantity
    #
    #         self.session.commit()
    #         messagebox.showinfo("Success", "Sale completed successfully!")
    #
    #         # Clear form
    #         self.sale_items.clear()
    #         for item in self.tree.get_children():
    #             self.tree.delete(item)
    #         self.customer_search.clear()
    #         self.update_total()
    #
    #     except Exception as e:
    #         self.session.rollback()
    #         messagebox.showerror("Error", f"Failed to complete sale: {str(e)}")

