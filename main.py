import tkinter as tk
from tkinter import ttk
from itertools import permutations, product, chain, zip_longest
from fractions import Fraction
import time

# Create the Tkinter main window
root = tk.Tk()
root.title("24 Point Referee")

# Initial 13 cards (A=1, 2-10, J=11, Q=12, K=13)
card_display_values = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
card_actual_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 
                      8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}


# Initialize variables for dropdown menus
card1, card2, card3, card4 = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

# Function to find a solution for 24-point game
def solve(digits):
    # Convert numbers to strings for easier handling
    digits = list(map(str, digits))
    num_len = len(digits)
    
    # Generate all permutations of the digits
    digit_permutations = sorted(set(permutations(digits)))
    
    # Generate all combinations of operators (+, -, *, /)
    operator_combinations = list(product('+-*/', repeat=num_len - 1))
    
    # Brackets positions for different combinations
    brackets = (
        [()] +  # No brackets
        [(x, y) for x in range(0, 2*num_len-1, 2) for y in range(x+4, 2*num_len+1, 2)]
    )
    
    # Iterate through permutations and operator combinations
    for digit_perm in digit_permutations:
        for ops in operator_combinations:
            # Use fractions for division to avoid floating-point errors
            expr_digits = [('Fraction(%s)' % d) if '/' in ops else d for d in digit_perm]
            # Create a basic expression without brackets
            expression = list(chain.from_iterable(zip_longest(expr_digits, ops, fillvalue='')))
            
            # Add brackets and evaluate each expression
            for b in brackets:
                expr_with_brackets = expression[:]
                for insert_index, bracket in zip(b, '()' * (len(b) // 2)):
                    expr_with_brackets.insert(insert_index, bracket)
                expr_str = ''.join(expr_with_brackets)
                
                try:
                    # Evaluate the expression
                    result = eval(expr_str)
                except ZeroDivisionError:
                    continue
                
                # Check if the result equals 24
                if result == 24:
                    # Format the output for readability
                    if '/' in ops:
                        expr_with_brackets = [
                            term if not term.startswith('Fraction(') else term[9:-1] 
                            for term in expr_with_brackets
                        ]
                    return ' '.join(expr_with_brackets).rstrip()
    return None

# Callback function for the "Submit" button
def solve_24_point():
    # Convert selected card values to integers
    selected_cards = [card_actual_values[card1.get()], card_actual_values[card2.get()],
                      card_actual_values[card3.get()], card_actual_values[card4.get()]]
    
    # Call the solve function and display the result
    result = solve(selected_cards)
    
    # Change background color and display result with animation
    if result:
        result_label.config(
            text="Calculating...",
            font=("Arial", 14, "bold"),
            background="yellow"
        )
        root.update()
        time.sleep(0.5)  # Simulate a delay to show the calculation process
        result_label.config(
            text=f"Solution: {result}",
            background="lightgreen"
        )
    else:
        result_label.config(
            text="Calculating...",
            font=("Arial", 14, "bold"),
            background="yellow"
        )
        root.update()
        time.sleep(0.5)  # Simulate a delay to show the calculation process
        result_label.config(
            text="No solution found!",
            background="lightcoral"
        )

# Create and place the dropdowns for selecting cards
for idx, card_var in enumerate([card1, card2, card3, card4], start=1):
    ttk.Label(root, text=f"Card {idx}").grid(column=0, row=idx-1, padx=10, pady=5)
    dropdown = ttk.Combobox(root, textvariable=card_var, values=card_display_values, state='readonly')
    dropdown.grid(column=1, row=idx-1, padx=10, pady=5)
    dropdown.set(card_display_values[0])  # Default selection

# Create the "Submit" button
submit_button = ttk.Button(root, text="Calculate", command=solve_24_point)
submit_button.grid(column=0, row=4, columnspan=2, pady=10)

# Label to display the result with a dynamic background color
result_label = tk.Label(root, text="", wraplength=300, font=("Arial", 14))
result_label.grid(column=0, row=5, columnspan=2, pady=10)

# Adjust window size for better layout
root.geometry("300x250")
root.resizable(False, False)
root.mainloop()
