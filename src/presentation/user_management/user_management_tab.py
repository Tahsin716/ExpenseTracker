from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager
from src.presentation.user_management.create_user_form import CreateUserForm
from src.presentation.user_management.update_user_form import UpdateUserForm


class UserManagementTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.user_manager = UserManager()

        self.action_frame = ttk.Frame(self)
        self.create_button = ttk.Button(self.action_frame, text="Create User", command=self.create_user)
        self.update_button = ttk.Button(self.action_frame, text="Update User", command=self.update_user)
        self.delete_button = ttk.Button(self.action_frame, text="Delete User", command=self.delete_user)
        self.create_button.pack(side='left', padx=5)
        self.update_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self, columns=('ID', 'First Name', 'Last Name', 'Email', 'Role'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('First Name', text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Role', text='Role')

        self.action_frame.pack(fill='x', pady=5)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_users()

    def refresh_users(self):
        users = self.user_manager.get_all_users()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users:
            self.tree.insert('', 'end', values=(user.user_id, user.first_name, user.last_name, user.email, user.role))


    def create_user(self):
        CreateUserForm(self, self.refresh_users)

    def update_user(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to update")
            return

        user_data = self.tree.item(selected_item[0], 'values')
        UpdateUserForm(self, user_data, self.refresh_users)

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        user_data = self.tree.item(selected_item[0], 'values')
        user_id = int(user_data[0])

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            success , message = self.user_manager.delete_user(user_id)

            if not success:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", "User successfully deleted")
                self.refresh_users()