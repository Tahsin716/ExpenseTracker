from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager


class UserManagementTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.user_manager = UserManager()

        self.tree = ttk.Treeview(self, columns=('ID', 'First Name', 'Last Name', 'Email', 'Role'))
        self.tree.heading('ID', text='ID')
        self.tree.heading('First Name', text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Role', text='Role')

        ttk.Button(self, text="Create User", command=self.create_user).pack()
        ttk.Button(self, text="Update User", command=self.update_user).pack()
        ttk.Button(self, text="Delete User", command=self.delete_user).pack()

        self.tree.pack(expand=True, fill='both')
        self.refresh_users()

    def refresh_users(self):
        users = self.user_manager.get_all_users()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users:
            self.tree.insert('', 'end', values=(user.user_id, user.first_name,
                                                user.last_name, user.email, user.role))

    def create_user(self):
        # Create user form window
        pass

    def update_user(self):
        # Update user form window
        pass

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            print("Hello")