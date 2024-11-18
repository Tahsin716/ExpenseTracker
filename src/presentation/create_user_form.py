import tkinter as tk
from tkinter import ttk


class CreateUserForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
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
        print("Save button clicked.")
        print(f"First Name: {self.first_name.get()}")
        print(f"Last Name: {self.last_name.get()}")
        print(f"Email: {self.email.get()}")
        print(f"Password: {self.password.get()}")
        print(f"Is Admin: {self.is_admin.get()}")

    def close_form(self):
        self.destroy()