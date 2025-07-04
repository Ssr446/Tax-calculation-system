import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database connection setup
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Initialize the database
def initialize_database(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            annual_income REAL NOT NULL,
                            deductions REAL NOT NULL,
                            regime TEXT CHECK (regime IN ('old', 'new')) NOT NULL,
                            tax_payable REAL NOT NULL
                        );''')

# Function to calculate tax
def calculate_tax(income, deductions, regime):
    taxable_income = income - deductions
    tax_payable = 0
    
    # Old Regime
    if regime == 'old':
        if taxable_income <= 250000:
            tax_payable = 0
        elif taxable_income <= 500000:
            tax_payable = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax_payable = 12500 + (taxable_income - 500000) * 0.2
        else:
            tax_payable = 112500 + (taxable_income - 1000000) * 0.3
    # New Regime
    elif regime == 'new':
        if taxable_income <= 250000:
            tax_payable = 0
        elif taxable_income <= 500000:
            tax_payable = (taxable_income - 250000) * 0.05
        elif taxable_income <= 750000:
            tax_payable = 12500 + (taxable_income - 500000) * 0.1
        elif taxable_income <= 1000000:
            tax_payable = 37500 + (taxable_income - 750000) * 0.15
        elif taxable_income <= 1250000:
            tax_payable = 75000 + (taxable_income - 1000000) * 0.2
        elif taxable_income <= 1500000:
            tax_payable = 125000 + (taxable_income - 1250000) * 0.25
        else:
            tax_payable = 187500 + (taxable_income - 1500000) * 0.3

    return tax_payable

# Function to save user data and calculated tax in the database
def save_user_data(conn, name, income, deductions, regime, tax_payable):
    sql = '''INSERT INTO users(name, annual_income, deductions, regime, tax_payable)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (name, income, deductions, regime, tax_payable))
    conn.commit()

# Function to display past tax calculations
def view_past_calculations(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    
    results_window = tk.Toplevel()
    results_window.title("Past Calculations")
    
    for idx, row in enumerate(rows):
        tk.Label(results_window, text=f"ID: {row[0]}, Name: {row[1]}, Income: {row[2]}, Deductions: {row[3]}, Regime: {row[4]}, Tax Payable: {row[5]}").grid(row=idx, column=0)

# Main function for Tkinter-based GUI
def main():
    db_file = "tax_calculator.db"
    conn = create_connection(db_file)
    initialize_database(conn)
    
    # Tkinter setup
    root = tk.Tk()
    root.title("Income Tax Calculator")

    # Input Fields
    tk.Label(root, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1)

    tk.Label(root, text="Annual Income").grid(row=1, column=0)
    income_entry = tk.Entry(root)
    income_entry.grid(row=1, column=1)

    tk.Label(root, text="Deductions").grid(row=2, column=0)
    deductions_entry = tk.Entry(root)
    deductions_entry.grid(row=2, column=1)

    tk.Label(root, text="Tax Regime").grid(row=3, column=0)
    regime_var = tk.StringVar(value="old")
    tk.Radiobutton(root, text="Old Regime", variable=regime_var, value="old").grid(row=3, column=1, sticky="w")
    tk.Radiobutton(root, text="New Regime", variable=regime_var, value="new").grid(row=3, column=2, sticky="w")

    # Function to calculate and display tax
    def calculate_and_save():
        name = name_entry.get()
        try:
            income = float(income_entry.get())
            deductions = float(deductions_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for income and deductions.")
            return
        
        regime = regime_var.get()
        tax_payable = calculate_tax(income, deductions, regime)
        save_user_data(conn, name, income, deductions, regime, tax_payable)
        messagebox.showinfo("Result", f"{name}, your calculated tax payable is: ₹{tax_payable:.2f}")

    # Calculate Button
    calculate_button = tk.Button(root, text="Calculate Tax", command=calculate_and_save)
    calculate_button.grid(row=4, column=1, pady=10)

    # View Past Calculations Button
    view_button = tk.Button(root, text="View Past Calculations", command=lambda: view_past_calculations(conn))
    view_button.grid(row=5, column=1, pady=5)

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
