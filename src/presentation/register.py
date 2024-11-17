from tkinter import ttk


class Register(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        fields = [('First Name:', 'first_name'), ('Last Name:', 'last_name'),
                  ('Email:', 'email'), ('Password:', 'password')]

        for i, (label, field) in enumerate(fields):
            ttk.Label(self, text=label).grid(row=i, column=0, pady=5, padx=5)
            entry = ttk.Entry(self)
            if field == 'password':
                entry.configure(show="*")
            entry.grid(row=i, column=1, pady=5, padx=5)
            setattr(self, field, entry)

        ttk.Button(self, text="Register", command=self.register_user).grid(row=len(fields), column=0, pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("Login")).grid(row=len(fields),
                                                                                                    column=1,
                                                                                                    pady=10)

    def register_user(self):
        first_name = self.first_name.get()
