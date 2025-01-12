from tkinter import ttk, messagebox

from src.business.services.customer_manager import CustomerManager
from src.business.services.inventory_manager import InventoryManager
from src.business.services.sale_manager import SaleManager
from src.business.services.user_manager import UserManager
from src.data_access.models.inventory_item import InventoryItem
from src.presentation.sales_management.add_item_dialog import AddItemDialog
from src.presentation.sales_management.search_dropdown import SearchDropdown


class SalesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.inventory_manager = InventoryManager()
        self.customer_manager = CustomerManager()
        self.sale_manager = SaleManager()

        customer_frame = ttk.LabelFrame(self, text="Customer Information")
        customer_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(customer_frame, text="Phone Number:").pack(side='left', padx=5)
        self.customer_search = SearchDropdown(
            customer_frame,
            "Enter phone number...",
            self.search_customers
        )
        self.customer_search.pack(side='left', padx=5)

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

        self.tree.column('ID', width=50)
        self.tree.column('Name', width=200)
        self.tree.column('Quantity', width=100)
        self.tree.column('Price', width=100)
        self.tree.column('Total', width=100)

        self.tree.pack(expand=True, fill='both', padx=5, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="Add Item",
            command=self.show_add_item_dialog,
            style="Create.TButton"
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_selected_item,
            style="Delete.TButton"
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Complete Sale",
            command=self.complete_sale,
            style="Update.TButton"
        ).pack(side='left', padx=5)

        total_frame = ttk.Frame(self)
        total_frame.pack(fill='x', padx=5, pady=5)

        self.total_label = ttk.Label(
            total_frame,
            text="Total: £0.00",
            font=('TkDefaultFont', 12, 'bold')
        )
        self.total_label.pack(side='left', padx=5)

        self.sale_items = {}

    def search_customers(self, phone_number : str) -> list[str]:
        customers = self.user_manager.search_customer_by_phone_number(phone_number)
        return [customer.phone_number for customer in customers]

    def search_items(self, search_text : str):
        items = self.inventory_manager.search_item_by_name(search_text)
        return [f"{item.name} (ID: {item.item_id}, Stock: {item.quantity})" for item in items]

    def get_item(self, item_id: int) -> InventoryItem:
        return self.inventory_manager.get_item_by_id(item_id)

    def show_add_item_dialog(self):
        AddItemDialog(self, self.search_items, self.add_item, self.get_item)

    def add_item(self, item : InventoryItem, quantity : int):
        item_id = item.item_id

        if item_id in self.sale_items:
            existing_qty = self.sale_items[item_id]['quantity']
            new_qty = existing_qty + quantity

            if new_qty > item.quantity:
                messagebox.showerror(
                    "Error",
                    f"Not enough stock. Available: {item.quantity}"
                )
                return

            self.sale_items[item_id]['item_id'] = item_id
            self.sale_items[item_id]['quantity'] : int = new_qty
            self.sale_items[item_id]['selling_price'] : float = item.selling_price
            self.sale_items[item_id]['total'] : float = new_qty * item.selling_price

            for child in self.tree.get_children():
                if self.tree.item(child)['values'][0] == item_id:
                    self.tree.item(
                        child,
                        values=(
                            item_id,
                            item.name,
                            new_qty,
                            f"£{item.selling_price:.2f}",
                            f"£{new_qty * item.selling_price:.2f}"
                        )
                    )
                    break
        else:
            self.sale_items[item_id] = {
                'item_id' : item_id,
                'quantity': quantity,
                'selling_price': item.selling_price,
                'total': quantity * item.selling_price
            }

            self.tree.insert(
                '',
                'end',
                values=(
                    item_id,
                    item.name,
                    quantity,
                    f"£{item.selling_price:.2f}",
                    f"£{quantity * item.selling_price:.2f}"
                )
            )

        self.update_total()

    def remove_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No items in selected")
            return

        item_id = self.tree.item(selected[0])['values'][0]
        del self.sale_items[item_id]
        self.tree.delete(selected[0])
        self.update_total()

    def reset_all_data(self):
        self.sale_items.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.customer_search.clear()
        self.update_total()

    def update_total(self):
        total = sum(item['total'] for item in self.sale_items.values())
        self.total_label.configure(text=f"Total: £{total:.2f}")

    def complete_sale(self):
        if not self.sale_items:
            messagebox.showwarning("Warning", "No items in sale")
            return

        phone_number = self.customer_search.get()
        customer = None

        if not phone_number or len(phone_number) == 0:
            messagebox.showwarning("Warning", "Customer phone number required")
            return

        if phone_number:
            customer = self.customer_manager.get_customer_by_phone_number(phone_number)

            if not customer:
                success, message, customer = self.customer_manager.create_customer(phone_number)

                if not success:
                    messagebox.showerror("Error", message)
                    return

        success, message, sale = self.sale_manager.create_sale(customer, self.sale_items)

        if not success:
            messagebox.showerror("Error", message)
            return

        messagebox.showinfo("Success", "Sale completed successfully!")
        self.reset_all_data()

