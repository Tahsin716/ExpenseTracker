from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager
from src.presentation.create_user_form import CreateUserForm


class UserManagementTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.user_manager = UserManager()

        self.tree = ttk.Treeview(self, columns=('ID', 'First Name', 'Last Name', 'Email', 'Role'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('First Name', text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Role', text='Role')

        self.action_frame = ttk.Frame(self)
        self.create_button = ttk.Button(self.action_frame, text="Create User", command=self.create_user)
        self.update_button = ttk.Button(self.action_frame, text="Update User", command=self.update_user)
        self.delete_button = ttk.Button(self.action_frame, text="Delete User", command=self.delete_user)
        self.create_button.pack(side='left', padx=5)
        self.update_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        self.action_frame.pack(fill='x', pady=5)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)

        self.refresh_users()

    def refresh_users(self):
        users = self.user_manager.get_all_users()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users:
            self.tree.insert('', 'end', values=(user.user_id, user.first_name, user.last_name, user.email, user.role))

    def on_row_select(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            self.action_frame.pack_forget()
        else:
            self.action_frame.pack(fill='x', pady=5)

    def create_user(self):
        CreateUserForm(self, self.refresh_users)

    def update_user(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to update")
            return

        user_data = self.tree.item(selected_item[0], 'values')
        print(f"Updating user: {user_data}")

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            print("Hello")