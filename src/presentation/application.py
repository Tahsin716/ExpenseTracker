import tkinter as tk
from tkinter import ttk

from src.presentation.auth.login import Login
from src.presentation.auth.register import Register
from src.presentation.main_page import MainPage


class Application:

    def __init__(self):
        root = tk.Tk()
        root.title("Coffee Shop")
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 50, root.winfo_screenheight() - 50))

        container = ttk.Frame()
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (Login, Register, MainPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")
        root.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if page_name == "MainPage":
            user_management_tab = frame.tabs["Users"]
            sales_tab = frame.tabs["Sales"]
            if user_management_tab:
                user_management_tab.refresh_users()

            if sales_tab:
                sales_tab.reset_all_data()

        frame.tkraise()



