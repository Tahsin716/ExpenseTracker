import tkinter as tk
from tkinter import ttk
from typing import Dict


class ExpenseReportDialog(tk.Toplevel):
    def __init__(self, parent, report_data: Dict):

        super().__init__(parent)
        self.title("Expense Report")
        self.geometry("500x500")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Expense Report", style='Title.TLabel').pack(pady=(0, 10))
        ttk.Label(main_frame, text=f"Total Expenses: {report_data['total_expenses']}",
                  style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Maximum Expense", style='Title.TLabel').pack(anchor='w')
        max_expense = report_data['max_expense']
        ttk.Label(main_frame,
                  text=f"Amount: ${max_expense['amount']:.2f}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Description: {max_expense['description']}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Date: {max_expense['date'].strftime('%Y-%m-%d')}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Category: {max_expense['category']}",
                  style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Minimum Expense", style='Title.TLabel').pack(anchor='w')
        min_expense = report_data['min_expense']
        ttk.Label(main_frame,
                  text=f"Amount: ${min_expense['amount']:.2f}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Description: {min_expense['description']}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Date: {min_expense['date'].strftime('%Y-%m-%d')}",
                  style='TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Category: {min_expense['category']}",
                  style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Most Common Category of Expense", style='Title.TLabel').pack(anchor='w')
        ttk.Label(main_frame,
                  text=f"Category: {report_data['most_common_category_id']}",
                  style='TLabel').pack(anchor='w')

        close_button = ttk.Button(main_frame, text="Close", command=self.destroy)
        close_button.pack(pady=20)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)