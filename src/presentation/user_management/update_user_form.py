import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager


class UpdateUserForm(tk.Toplevel):
    def __init__(self, parent, user_data, callback):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.title("Update User")
        self.geometry("400x300")

        self.user_data = user_data
        self.callback = callback  # Callback to refresh users

        self.first_name = tk.StringVar(value=user_data[1])
        self.last_name = tk.StringVar(value=user_data[2])
        self.email = tk.StringVar(value=user_data[3])

        ttk.Label(self, text="First Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.first_name).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Last Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.last_name).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Email").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.email).grid(row=2, column=1, padx=10, pady=5)


        ttk.Button(self, text="Update", command=self.save_user).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=5, column=1, padx=10, pady=10)

    def save_user(self):
        user_id = int(self.user_data[0])
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        email = self.email.get()

        success, message, user = self.user_manager.update_user(user_id, first_name, last_name, email)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "User updated successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()
