import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import re

# Load expenses from a text file
def load_expenses(filename):
    expenses = []  # Initialize an empty list for expenses
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split each line into components and append to the expenses list
                title, date, amount, description, payment_method = line.strip().split(" | ")
                expenses.append((title, date, float(amount), description, payment_method))
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
    return expenses

# Save expenses to a text file
def save_expenses(filename, expenses):
    with open(filename, 'w') as file:
        for title, date, amount, description, payment_method in expenses:
            # Write each expense to the file in a formatted string
            file.write(f"{title} | {date} | {amount} | {description} | {payment_method}\n")

# Update the displayed expenses and total amount
def update_expense_display():
    expense_list.delete(0, tk.END)  # Clear the current display
    total = 0  # Initialize total to 0
    for title, date, amount, description, payment_method in expenses:
        # Insert each expense into the Listbox and calculate the total
        expense_list.insert(tk.END, f"{title} - {date} - ${amount:.2f} - {description} - {payment_method}")
        total += amount
    total_expense.set(f"Total Expense: ${total:.2f}")  # Update total expense display

# Validate date format to ensure it is in YYYY-MM-DD
def is_valid_date(date_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'  # Regular expression pattern for date validation
    return re.match(pattern, date_string)  # Return True if date matches the pattern

# Add an expense to the list
def add_expense():
    # Get values from the input fields
    title = category_var.get()
    date_value = date_entry.get()
    amount_value = amount_entry.get()
    description_value = description_entry.get()
    payment_method_value = payment_method_var.get()

    # Check if all fields are filled
    if title and date_value and amount_value and description_value and payment_method_value:
        if is_valid_date(date_value):  # Validate date format
            try:
                amount_value = float(amount_value)  # Convert amount to float
                if amount_value >= 0:  # Ensure amount is non-negative
                    # Append the new expense to the list
                    expenses.append((title, date_value, amount_value, description_value, payment_method_value))
                    update_expense_display()  # Refresh the displayed expenses
                    clear_inputs()  # Clear the input fields
                    save_expenses('expenses.txt', expenses)  # Save the updated expenses to file
                else:
                    messagebox.showerror("Invalid Input", "Amount must be non-negative.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        else:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
    else:
        messagebox.showerror("Invalid Input", "Please fill all fields.")

# Clear input fields after adding an expense
def clear_inputs():
    category_combobox.set('Select Category')  # Reset category selection
    date_entry.delete(0, tk.END)  # Clear date entry
    amount_entry.delete(0, tk.END)  # Clear amount entry
    description_entry.delete(0, tk.END)  # Clear description entry
    payment_method_combobox.set('Select Payment Method')  # Reset payment method selection

# Remove the selected expense from the list
def remove_expense():
    selected_index = expense_list.curselection()  # Get the index of the selected expense
    if selected_index:
        selected_text = expense_list.get(selected_index)  # Get the selected expense text
        try:
            # Split the selected text to extract individual components
            parts = selected_text.split(" - ")
            title, date_value, amount_value, description, payment_method = parts[0], parts[1], parts[2].split("$")[1], parts[3], parts[4]
            amount_value = float(amount_value)  # Convert extracted amount to float
            # Remove the selected expense from the expenses list
            expenses.remove((title, date_value, amount_value, description, payment_method))
            update_expense_display()  # Refresh the displayed expenses
            save_expenses('expenses.txt', expenses)  # Save the updated expenses to file
        except (ValueError, IndexError):
            messagebox.showerror("Remove Error", "Could not remove the selected expense.")
    else:
        messagebox.showerror("Remove Error", "Please select an expense to remove.")

# Visualize expenses in a bar chart
def visualize_expenses():
    if not expenses:
        messagebox.showinfo("Info", "No expenses to visualize.")  # Show info if there are no expenses
        return

    # Prepare data for visualization
    titles = [title for title, _, _, _, _ in expenses]
    amounts = [amount for _, _, amount, _, _ in expenses]

    plt.figure(figsize=(10, 5))  # Set the figure size
    plt.bar(titles, amounts, color='skyblue')  # Create a bar chart
    plt.xlabel('Categories')  # Label for x-axis
    plt.ylabel('Amounts')  # Label for y-axis
    plt.title('Expense Visualization')  # Title of the chart
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()  # Display the chart

# Load expenses from file on startup
expenses = load_expenses('expenses.txt')

# Initialize the main window
root = tk.Tk()
root.title("Personal Expense Tracker")  # Set the window title
root.geometry("700x550+100+100")  # Set window size and position
root.resizable(False, False)  # Disable window resizing
root.configure(bg="#f0f0f0")  # Set background color

# Variables for total expense display
total_expense = tk.StringVar()
total_expense.set("Total Expense: $0.00")  # Initialize total expense display

# Dropdown categories
categories = ["Food", "Travel", "Shopping", "Recharge", "Entertainment", "Other"]
category_var = tk.StringVar()

# Dropdown payment methods
payment_methods = ["Cash", "Credit Card", "Debit Card", "Online", "Other"]
payment_method_var = tk.StringVar()

# Create frames for better organization
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)  # Add padding for aesthetics

display_frame = tk.Frame(root, bg="#f0f0f0")
display_frame.pack(pady=10)  # Add padding for aesthetics

# GUI Elements for input frame
tk.Label(input_frame, text="Hello User!", font=("Comic Sans MS", 16, "bold"), fg="black", bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(input_frame, text="Select Category", font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, sticky="w")
category_combobox = ttk.Combobox(input_frame, textvariable=category_var, font=("Comic Sans MS", 10), values=categories, state="readonly")
category_combobox.grid(row=1, column=1, padx=5, pady=5)
category_combobox.set("Select Category")  # Default text

tk.Label(input_frame, text="Enter Date (YYYY-MM-DD)", font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").grid(row=2, column=0, sticky="w")
date_entry = tk.Entry(input_frame, font=("Comic Sans MS", 10), width=25)
date_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Enter Amount", font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").grid(row=3, column=0, sticky="w")
amount_entry = tk.Entry(input_frame, font=("Comic Sans MS", 10), width=25)
amount_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Enter Description", font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").grid(row=4, column=0, sticky="w")
description_entry = tk.Entry(input_frame, font=("Comic Sans MS", 10), width=25)
description_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Select Payment Method", font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").grid(row=5, column=0, sticky="w")
payment_method_combobox = ttk.Combobox(input_frame, textvariable=payment_method_var, font=("Comic Sans MS", 10), values=payment_methods, state="readonly")
payment_method_combobox.grid(row=5, column=1, padx=5, pady=5)
payment_method_combobox.set("Select Payment Method")  # Default text

# Buttons
button_frame = tk.Frame(input_frame, bg="#f0f0f0")
button_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Add", font=("Comic Sans MS", 10, "bold"), bg="#90ee90", command=add_expense, width=10).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove", font=("Comic Sans MS", 10, "bold"), bg="#ffcccb", command=remove_expense, width=10).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Visualize", font=("Comic Sans MS", 10, "bold"), bg="#add8e6", command=visualize_expenses, width=10).grid(row=0, column=2, padx=5)

# GUI Elements for display frame
tk.Label(display_frame, textvariable=total_expense, font=("Comic Sans MS", 10, "bold"), bg="#f0f0f0").pack(pady=5)

# Change Text widget to Listbox for selectable expenses
expense_list = tk.Listbox(display_frame, font=("Comic Sans MS", 10), fg="black", bg='white', height=10, width=70)
expense_list.pack(pady=10)

# Start the GUI event loop
update_expense_display()  # Ensure expenses are displayed at startup
root.mainloop()  # Run the application
