from tkinter import ttk


class Login(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Create widgets
        ttk.Label(self, text="Email:").grid(row=0, column=0, pady=5, padx=5)
        self.email = ttk.Entry(self)
        self.email.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self, text="Password:").grid(row=1, column=0, pady=5, padx=5)
        self.password = ttk.Entry(self, show="*")
        self.password.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).grid(row=2, column=1,
                                                                                                      pady=10)

    def login(self):
        email = self.email.get()
        password = self.password.get()

