from tkinter import ttk

from src.business.services.inventory_manager import InventoryManager


class InventoryManagementTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.inventory_manager = InventoryManager()

        self.action_frame = ttk.Frame(self)
        self.create_button = ttk.Button(self.action_frame, text="Create Inventory", command=self.create_inventory_item)
        self.update_button = ttk.Button(self.action_frame, text="Update Inventory", command=self.update_inventory_item)
        self.delete_button = ttk.Button(self.action_frame, text="Delete Inventory", command=self.delete_inventory_item)
        self.create_button.pack(side='left', padx=5)
        self.update_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Description', 'Quantity', 'Cost Price', 'Selling Price'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Cost Price', text='Cost Price')
        self.tree.heading('Selling Price', text='Selling Price')

        self.action_frame.pack(fill='x', pady=5)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_users()

    def refresh_users(self):
        items = self.inventory_manager.get_all_inventory_items()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in items:
            self.tree.insert('', 'end', values=(item.item_id, item.name, item.description, item.quantity, item.cost_price, item.selling_price))


    def create_inventory_item(self):
        pass

    def update_inventory_item(self):
        pass

    def delete_inventory_item(self):
        pass