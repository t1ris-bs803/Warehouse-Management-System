Warehouse Management System (CLI)
================================

A simple warehouse inventory management system built with Python.
This project runs in a command-line interface (CLI) and manages
product inventory by location using a JSON file for persistent storage.

The system is designed to be easily extendable.
The next planned steps are Flask server integration and a GUI application.


Features
--------

1. Add Inventory
   - Add products to a specific warehouse location.
   - Automatically creates locations if they do not exist.

2. Remove Inventory
   - Remove product quantities from a specific location.
   - Prevents removal if stock is insufficient.

3. Product Lookup
   - Search inventory by product name.
   - Displays all locations and quantities for the product.

4. Move Inventory
   - Move products between locations.
   - Automatically cleans up empty products and locations.

5. Persistent Storage
   - Inventory data is saved in a JSON file (`storage.json`).
   - Data remains after program restart.


Data Structure
--------------

Example of `storage.json`:

{
    "A-1/1/1": {
        "Bolt": 50,
        "Nut": 30
    },
    "B-2/3/1": {
        "Bolt": 20
    }
}

- Top-level key: Location
- Second-level key: Product name
- Value: Quantity


Location Format
---------------

Locations must be entered using the following format:

Warehouse-Floor/Row/Column

Example:
A-1/2/3
B-2/1/4


How to Run
----------

1. Install Python 3.x
2. Run the program

python wmy.korean.py

※ `storage.json` will be created automatically on first run.


Technologies Used
-----------------

- Python 3
- JSON file storage
- Command Line Interface (CLI)
