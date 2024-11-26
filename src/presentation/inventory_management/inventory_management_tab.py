from tkinter import ttk, messagebox

from src.business.services.inventory_manager import InventoryManager
from src.presentation.inventory_management.create_inventory_form import CreateInventoryForm
from src.presentation.inventory_management.update_inventory_form import UpdateInventoryForm


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

        self.refresh_data()

    def refresh_data(self):
        items = self.inventory_manager.get_all_inventory_items()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in items:
            self.tree.insert('', 'end', values=(item.item_id, item.name, item.description, item.quantity, item.cost_price, item.selling_price))


    def create_inventory_item(self):
        CreateInventoryForm(self, self.refresh_data)

    def update_inventory_item(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to update")
            return

        user_data = self.tree.item(selected_item[0], 'values')
        UpdateInventoryForm(self, user_data, self.refresh_data)

    def delete_inventory_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return

        user_data = self.tree.item(selected_item[0], 'values')

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            success, message = self.inventory_manager.delete_item(user_data[0])

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "Item successfully deleted")
                self.refresh_data()