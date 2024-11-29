import tkinter as tk
from tkinter import ttk
from typing import Dict

class RevenueReportDialog(tk.Toplevel):
    def __init__(self, parent, report_data: Dict):
        super().__init__(parent)
        self.title("Revenue Report")
        self.geometry("500x550")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Metric.TLabel', font=('Arial', 10, 'bold'))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Revenue Report", style='Title.TLabel').pack(pady=(0,10))

        ttk.Label(main_frame, text=f"Number of Sales: {report_data['number_of_sales']}", style='Metric.TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Expense Metrics", style='Title.TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Total Expense: ${report_data['total_expenses']:.2f}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Inventory Metrics", style='Title.TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Total Inventory Cost: ${report_data['total_inventory_cost']:.2f}", style='TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Total Inventory Selling Value: ${report_data['total_inventory_selling_value']:.2f}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Revenue", style='Title.TLabel').pack(anchor='w')
        ttk.Label(main_frame, text=f"Revenue generated from sales: ${report_data['total_revenue']:.2f}", style='TLabel').pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Profit from Sales", style='Title.TLabel').pack(anchor='w')
        profit_from_sales = ttk.Label(
            main_frame,
            text=f"Profit: ${report_data['profit_from_sold_items']:.2f}",
            style='Metric.TLabel',
            foreground='green' if report_data['profit_from_sold_items'] >= 0 else 'red'
        )
        profit_from_sales.pack(anchor='w')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(main_frame, text="Net Profit", style='Title.TLabel').pack(anchor='w')
        net_profit = ttk.Label(
            main_frame,
            text=f"Profit: ${report_data['net_profit']:.2f}",
            style='Metric.TLabel',
            foreground='green' if report_data['net_profit'] >= 0 else 'red'
        )
        net_profit.pack(anchor='w')

        close_button = ttk.Button(main_frame, text="Close", command=self.destroy)
        close_button.pack(pady=20)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
