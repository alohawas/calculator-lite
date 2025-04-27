import tkinter as tk
import math
from sympy import symbols, diff, integrate, sin, cos, sympify, SympifyError

x = symbols('x')

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        
        # Configure grid weights for better resizing
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
        # Entry widget for display
        self.entry = tk.Entry(root, width=40, borderwidth=5, font=('Arial', 16))
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Create buttons
        self.create_buttons()
        
    def create_buttons(self):
        # Define button layout with better organization
        button_rows = [
            # Row 1: Basic operations
            ['7', '8', '9', '/'],
            # Row 2: Basic operations
            ['4', '5', '6', '*'],
            # Row 3: Basic operations
            ['1', '2', '3', '-'],
            # Row 4: Basic operations and clear
            ['0', 'C', '=', '+'],
            # Row 5: Trig functions and exponent
            ['sin', 'cos', 'tan', '^'],
            # Row 6: Parentheses and constants
            ['(', ')', 'π', 'e'],
            # Row 7: Calculus and advanced functions
            ['d/dx', '∫dx', 'log', '√']
        ]
        
        # Create buttons with consistent styling
        button_style = {
            'font': ('Arial', 12),
            'width': 8,
            'height': 2,
            'bd': 3,
            'relief': tk.RAISED
        }
        
        for row_idx, row in enumerate(button_rows, start=1):
            for col_idx, text in enumerate(row):
                if text == '=':
                    button = tk.Button(self.root, text=text, **button_style, 
                                     command=self.calculate_result)
                elif text == 'C':
                    button = tk.Button(self.root, text=text, **button_style, 
                                     command=self.clear_entry)
                elif text == 'd/dx':
                    button = tk.Button(self.root, text=text, **button_style, 
                                     command=self.calculate_derivative)
                elif text == '∫dx':
                    button = tk.Button(self.root, text=text, **button_style, 
                                     command=self.calculate_integral)
                else:
                    button = tk.Button(self.root, text=text, **button_style, 
                                     command=lambda t=text: self.press_button(t))
                
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")
    
    def press_button(self, button_text):
        current = self.entry.get()
        
        # Handle special symbols
        special_mappings = {
            'π': str(math.pi),
            'e': str(math.e),
            '^': '**',
            '√': 'math.sqrt(',
            'sin': 'math.sin(',
            'cos': 'math.cos(',
            'tan': 'math.tan(',
            'log': 'math.log10('
        }
        
        button_text = special_mappings.get(button_text, button_text)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current + button_text)
    
    def clear_entry(self):
        self.entry.delete(0, tk.END)
    
    def calculate_result(self):
        try:
            expression = self.entry.get()
            # Replace common math functions
            expression = expression.replace('^', '**')
            result = str(eval(expression))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
    
    def calculate_derivative(self):
        try:
            expression = sympify(self.entry.get())
            result = diff(expression, x)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except SympifyError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Invalid expression")
    
    def calculate_integral(self):
        try:
            expression = sympify(self.entry.get())
            result = integrate(expression, x)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except SympifyError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Invalid expression")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")  # Set a reasonable initial size
    calculator = Calculator(root)
    root.mainloop()