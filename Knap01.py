import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def knapsack(values, weights, capacity, n):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            item_weight = weights[i - 1]
            item_value = values[i - 1]
            
            if item_weight <= w:
                dp[i][w] = max(item_value + dp[i - 1][w - item_weight], 
                               dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity
    max_total_value = dp[n][capacity]
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
            
    selected.reverse()
    return max_total_value, selected

# --- Visualization Function ---
def visualize(values, weights, selected):
    """
    Creates a bar chart to visualize the value of all items, 
    highlighting the selected items.
    """
    item_labels = [f"Item {i+1}\n(W:{weights[i]})" for i in range(len(values))]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(len(values)), values, 
                   color=['#4CAF50' if i in selected else '#B0BEC5' for i in range(len(values))],
                   edgecolor='black')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), 
                 ha='center', va='bottom', fontsize=9)

    plt.xticks(range(len(values)), item_labels)
    plt.xlabel("Item Index and Weight (W)", fontsize=12)
    plt.ylabel("Value (V)", fontsize=12)
    plt.title("Knapsack Item Selection (Green = Chosen)", fontsize=14, weight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- GUI Logic and Solver Function ---
def solve_knapsack():
    result_text_widget.config(state=tk.NORMAL)     
    result_text_widget.delete('1.0', tk.END) 
    
    try:
        values_str = value_entry.get().strip()
        weights_str = weight_entry.get().strip()
        capacity_str = capacity_entry.get().strip()

        if not values_str or not weights_str or not capacity_str:
            messagebox.showwarning("Warning", "All fields must be filled.")
            result_text_widget.config(state=tk.DISABLED) 
            return

        values = [int(x) for x in values_str.split()]
        weights = [int(x) for x in weights_str.split()]
        capacity = int(capacity_str)

        if len(values) != len(weights):
            messagebox.showerror("Error", "Values and Weights must have the exact same number of elements!")
            result_text_widget.config(state=tk.DISABLED) 
            return
        
        if any(v <= 0 for v in values) or any(w <= 0 for w in weights):
             messagebox.showerror("Error", "Values and Weights must be positive integers.")
             result_text_widget.config(state=tk.DISABLED) 
             return
             
        if capacity <= 0:
            messagebox.showerror("Error", "Capacity must be a positive integer.")
            result_text_widget.config(state=tk.DISABLED) 
            return

        n = len(values)
        
        max_value, selected_indices = knapsack(values, weights, capacity, n)
        
        selected_items_info = []
        total_weight = 0
        
        for index in selected_indices:
            selected_items_info.append(f"Item {index + 1} (V:{values[index]}, W:{weights[index]})")
            total_weight += weights[index]
            
        selected_items_str = "\n".join(selected_items_info) if selected_items_info else "No items selected."

        result_text = (
            f"💰 Maximum Profit Achieved: {max_value}\n"
            f"⚖️ Total Weight Used: {total_weight} / {capacity}\n"
            f"\nChosen Items Details (Index, Value, Weight):\n"
            f"{selected_items_str}"
        )
        result_text_widget.insert(tk.END, result_text)
        visualize(values, weights, selected_indices)

    except ValueError:
        messagebox.showerror("Error", "Please ensure all entries are valid integers separated by spaces, and capacity is an integer.")
    except Exception as e:
        messagebox.showerror("An unexpected error occurred", str(e))
    finally:
        result_text_widget.config(state=tk.DISABLED)


# --- Main Application Setup ---
root = tk.Tk()
root.title("🎒 0/1 Knapsack Problem Solver")
root.geometry("500x600")
root.configure(bg='#ECEFF1')

tk.Label(root, text="Knapsack Optimization Solver", 
         font=("Helvetica", 16, "bold"), bg='#B0BEC5', fg='black', padx=10, pady=10).pack(fill='x', pady=(10, 5))

tk.Label(root, text="Goal: Maximize the total value of items without exceeding the knapsack's capacity. Enter values as space-separated integers.", 
         font=("Arial", 10), wraplength=450, justify='center', bg='#ECEFF1').pack(pady=(0, 10))

# Input Frames
input_frame = tk.Frame(root, bg='#ECEFF1')
input_frame.pack(pady=10, padx=20, fill='x')

tk.Label(input_frame, text="✅ Item Values (V):", font=("Arial", 11, "bold"), bg='#ECEFF1').pack(anchor='w')
value_entry = tk.Entry(input_frame, width=50, bd=2, relief=tk.GROOVE)
value_entry.pack(pady=3, ipady=3)
value_entry.insert(0, "10 40 30 50 25 15 35 45 5 55")
tk.Label(input_frame, text="⚖️ Item Weights (W):", font=("Arial", 11, "bold"), bg='#ECEFF1').pack(anchor='w', pady=(10, 0))
weight_entry = tk.Entry(input_frame, width=50, bd=2, relief=tk.GROOVE)
weight_entry.pack(pady=3, ipady=3)
weight_entry.insert(0, "5 4 6 3 2 1 7 8 9 10") 

tk.Label(input_frame, text="📦 Knapsack Capacity (C):", font=("Arial", 11, "bold"), bg='#ECEFF1').pack(anchor='w', pady=(10, 0))
capacity_entry = tk.Entry(input_frame, width=20, bd=2, relief=tk.GROOVE)
capacity_entry.pack(pady=3, ipady=3)
capacity_entry.insert(0, "20") 

tk.Button(root, text="SOLVE KNAPSACK", command=solve_knapsack, 
          font=("Helvetica", 12, "bold"), bg='#4CAF50', fg='white', relief=tk.RAISED, bd=3, padx=20, pady=5).pack(pady=15)


result_frame = tk.Frame(root, padx=20, pady=10, bg='#ECEFF1')
result_frame.pack(fill='x', padx=20, pady=10)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text_widget = tk.Text(result_frame, font=("Consolas", 10), wrap=tk.WORD, 
                             yscrollcommand=scrollbar.set, height=10, 
                             bd=2, relief=tk.SUNKEN, padx=5, pady=5)
result_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

initial_text = "Results will be shown here. \n(A graph will also appear)."
result_text_widget.insert(tk.END, initial_text)

scrollbar.config(command=result_text_widget.yview)

result_text_widget.config(state=tk.DISABLED) 

root.mainloop()
