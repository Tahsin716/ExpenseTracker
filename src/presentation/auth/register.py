import tkinter as tk
from tkinter import ttk, messagebox

from src.business.services.user_manager import UserManager


class Register(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_manager = UserManager()

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.is_admin = tk.BooleanVar()

        fields = [('First Name:', 'first_name'), ('Last Name:', 'last_name'),
                  ('Email:', 'email'), ('Password:', 'password'), ('Is Admin:', 'is_admin')]

        ttk.Label(self, text="First Name:").grid(row=0, column=0, pady=5, padx=5)
        self.first_name = ttk.Entry(self)
        self.first_name.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self, text="Last Name:").grid(row=1, column=0, pady=5, padx=5)
        self.last_name = ttk.Entry(self)
        self.last_name.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self, text="Email:").grid(row=2, column=0, pady=5, padx=5)
        self.email = ttk.Entry(self)
        self.email.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self, text="Password:").grid(row=3, column=0, pady=5, padx=5)
        self.password = ttk.Entry(self)
        self.password.configure(show="*")
        self.password.grid(row=3, column=1, pady=5, padx=5)

        ttk.Checkbutton(self, text="Is Admin", variable=self.is_admin).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self, text="Register", command=self.register_user).grid(row=len(fields), column=0, pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("Login")).grid(row=len(fields),
                                                                                                    column=1,
                                                                                                    pady=10)

    def register_user(self):
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        email = self.email.get()
        password = self.password.get()
        is_admin = self.is_admin.get()

        success, message, user = self.user_manager.register(first_name, last_name, password, email, is_admin)

        if not success:
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Success", "User created successfully!")
            self.controller.show_frame("MainPage")

