import tkinter as tk
from tkinter import ttk

class InventorySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System")

        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.inventory_tab = ttk.Frame(self.tabs)
        self.sales_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.inventory_tab, text="Inventory")
        self.tabs.add(self.sales_tab, text="Sales")
        self.tabs.pack(expand=1, fill="both")

        # Create widgets for the Inventory tab
        self.create_inventory_widgets()

        # Create widgets for the Sales tab
        self.create_sales_widgets()

    def create_inventory_widgets(self):
        # Example: Labels, Entry, and Button for adding items to inventory
        ttk.Label(self.inventory_tab, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(self.inventory_tab)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.inventory_tab, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.inventory_tab)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.inventory_tab, text="Add to Inventory", command=self.add_to_inventory).grid(row=2, column=0, columnspan=2, pady=10)

        # TODO: Add more widgets based on the requirements of the inventory system

    def create_sales_widgets(self):
        # TODO: Create widgets for the Sales tab based on the requirements
        pass

    def add_to_inventory(self):
        # TODO: Implement the logic to add items to the inventory
        product_name = self.product_name_entry.get()
        quantity = int(self.quantity_entry.get())

        # Example: Print the added item to the console (replace with actual logic)
        print(f"Added to Inventory: Product Name - {product_name}, Quantity - {quantity}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystemGUI(root)
    root.mainloop()