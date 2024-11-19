import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager


class CreateUserForm(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.callback = callback
        self.title("Create User")
        self.geometry("400x300")

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.is_admin = tk.BooleanVar()

        ttk.Label(self, text="First Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.first_name).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Last Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.last_name).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="Email").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.email).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Password").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.password, show="*").grid(row=3, column=1, padx=10, pady=5)

        ttk.Checkbutton(self, text="Is Admin", variable=self.is_admin).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self, text="Save", command=self.save_user).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.close_form).grid(row=5, column=1, padx=10, pady=10)

    def save_user(self):
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        email = self.email.get()
        password = self.password.get()
        is_admin = self.is_admin.get()

        success, message, user = self.user_manager.register(first_name, last_name, password, email, is_admin)

        if not success:
            messagebox.showerror("Error", message)
            self.focus()
        else:
            messagebox.showinfo("Success", "User created successfully!")
            self.callback()
            self.close_form()

    def close_form(self):
        self.destroy()
