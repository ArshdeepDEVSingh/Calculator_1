import tkinter as tk
from tkinter import ttk

# Function to handle button clicks
def button_click(entry_widget, value):
    if value == "C":
        entry_widget.delete(0, tk.END)
    elif value == "⌫":
        current = entry_widget.get()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, current[:-1])  # Remove the last character
    elif value == "=":
        calculate_result()
    else:
        entry_widget.insert(tk.END, value)

# Restrict input to valid characters
def validate_input(action, char):
    if action == "1":  # Input action
        return char.isdigit() or char in ".+-*/"
    return True

# Calculate the result of the entered expression
def calculate_result():
    try:
        result = eval(entry.get())  # Evaluate the expression
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Storage conversion function
def convert_storage():
    try:
        value = float(entry_storage.get())
        from_unit = combo_storage_from.get()
        to_unit = combo_storage_to.get()
        units = {"Bytes": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
        result = value * units[from_unit] / units[to_unit]
        label_storage_result.config(text=f"{result:.2f} {to_unit}")
    except ValueError:
        label_storage_result.config(text="Invalid Input")

# Currency conversion function
def convert_currency():
    try:
        value = float(entry_currency.get())
        from_currency = combo_currency_from.get()
        to_currency = combo_currency_to.get()

        # Exchange rates relative to USD
        rates = {
            "USD": 1, "EUR": 0.85, "INR": 74.85, "GBP": 0.75,
            "JPY": 110.0, "CAD": 1.25, "AUD": 1.35
        }
        result = value * rates[to_currency] / rates[from_currency]
        label_currency_result.config(text=f"{result:.2f} {to_currency}")
    except ValueError:
        label_currency_result.config(text="Invalid Input")

# Keyboard support
def key_press(event):
    key = event.char
    if key in "0123456789.+-*/":
        entry.insert(tk.END, key)
    elif event.keysym == "Return":
        calculate_result()
    elif event.keysym == "BackSpace":
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current[:-1])
    return "break"  # Prevent default behavior to avoid duplicate input

# Main window setup
root = tk.Tk()
root.title("Calculator")
root.geometry("400x600")
root.minsize(400, 600)
root.config(bg="#202124")

# Tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

validate_cmd = (root.register(validate_input), "%d", "%S")  # Restrict input

# Calculator Tab
frame_calculator = ttk.Frame(notebook)
notebook.add(frame_calculator, text="Calculator")

entry = ttk.Entry(frame_calculator, font=("Segoe UI", 24), justify="right", validate="key", validatecommand=validate_cmd)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

button_style = {"font": ("Segoe UI", 14), "width": 6, "height": 2, "relief": "flat"}
bg_color = "#2B2D2F"
fg_color = "#FFFFFF"
accent_color = "#F89E3B"

buttons = [
    ("C", 1, 0), ("⌫", 1, 1), ("(", 1, 2), (")", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
    ("0", 5, 0), (".", 5, 1), ("=", 5, 2), ("+", 5, 3),
]

for (text, row, col) in buttons:
    btn = tk.Button(
        frame_calculator, text=text,
        bg=bg_color if text not in ["=", "⌫"] else accent_color,
        fg=fg_color,
        activebackground="#3C4043", activeforeground="#FFFFFF",
        command=lambda t=text: button_click(entry, t),
        **button_style
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(6):
    frame_calculator.grid_rowconfigure(i, weight=1)
for j in range(4):
    frame_calculator.grid_columnconfigure(j, weight=1)

# Storage Converter Tab
frame_storage = ttk.Frame(notebook)
notebook.add(frame_storage, text="Storage Converter")

entry_storage = ttk.Entry(frame_storage, validate="key", validatecommand=validate_cmd)
entry_storage.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

combo_storage_from = ttk.Combobox(frame_storage, values=["Bytes", "KB", "MB", "GB", "TB"])
combo_storage_from.set("MB")
combo_storage_from.grid(row=1, column=0, padx=5, pady=5)

combo_storage_to = ttk.Combobox(frame_storage, values=["Bytes", "KB", "MB", "GB", "TB"])
combo_storage_to.set("GB")
combo_storage_to.grid(row=1, column=1, padx=5, pady=5)

btn_convert_storage = ttk.Button(frame_storage, text="Convert", command=convert_storage)
btn_convert_storage.grid(row=2, column=0, columnspan=2, pady=10)

label_storage_result = ttk.Label(frame_storage, text="")
label_storage_result.grid(row=3, column=0, columnspan=2, pady=10)

# Currency Converter Tab
frame_currency = ttk.Frame(notebook)
notebook.add(frame_currency, text="Currency Converter")

entry_currency = ttk.Entry(frame_currency, validate="key", validatecommand=validate_cmd)
entry_currency.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

combo_currency_from = ttk.Combobox(frame_currency, values=["USD", "EUR", "INR", "GBP", "JPY", "CAD", "AUD"])
combo_currency_from.set("USD")
combo_currency_from.grid(row=1, column=0, padx=5, pady=5)

combo_currency_to = ttk.Combobox(frame_currency, values=["USD", "EUR", "INR", "GBP", "JPY", "CAD", "AUD"])
combo_currency_to.set("INR")
combo_currency_to.grid(row=1, column=1, padx=5, pady=5)

btn_convert_currency = ttk.Button(frame_currency, text="Convert", command=convert_currency)
btn_convert_currency.grid(row=2, column=0, columnspan=2, pady=10)

label_currency_result = ttk.Label(frame_currency, text="")
label_currency_result.grid(row=3, column=0, columnspan=2, pady=10)

# Keyboard bindings
entry.bind("<Key>", key_press)  # Bind only to the entry to ensure proper event handling

root.mainloop()
