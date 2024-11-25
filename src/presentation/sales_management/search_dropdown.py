import tkinter as tk
from tkinter import ttk


class SearchDropdown(ttk.Frame):
    def __init__(self, parent, placeholder, search_function):
        super().__init__(parent)

        self.search_function = search_function
        self.placeholder = placeholder

        # Create Entry widget for user input
        self.entry = ttk.Entry(self, width=30)
        self.entry.insert(0, placeholder)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyRelease>', self.on_type)
        self.entry.pack(side='top', fill='x', padx=5, pady=(5, 0))

        # Create Listbox for suggestions
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.pack(side='top', fill='x', padx=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<FocusOut>', lambda e: self.listbox.pack_forget())
        self.listbox.pack_forget()  # Hide initially

        self.first_click = True
        self.selected_item = None

    def on_focus_in(self, event):
        if self.first_click and self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.first_click = False

    def on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.first_click = True
            self.listbox.pack_forget()  # Hide suggestions when focus is lost

    def on_type(self, event):
        current_text = self.entry.get()

        # Clear listbox if empty input
        if not current_text.strip() or current_text == self.placeholder:
            self.listbox.pack_forget()
            return

        # Get matching items
        matching_items = self.search_function(current_text)

        if matching_items:
            self.listbox.delete(0, tk.END)
            for item in matching_items:
                self.listbox.insert(tk.END, item)

            self.listbox.pack(side='top', fill='x')  # Show the listbox
        else:
            self.listbox.pack_forget()

    def on_select(self, event):
        if self.listbox.curselection():
            self.selected_item = self.listbox.get(self.listbox.curselection()[0])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.selected_item)
            self.listbox.pack_forget()

    def get(self):
        value = self.entry.get()
        return None if value == self.placeholder else value

    def clear(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.selected_item = None
        self.first_click = True

