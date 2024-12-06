import json
import sqlite3

db_file = 'db.sqlite'

def initialize_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Create customers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        ''')

        # Create items table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
        ''')

        # Create orders table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
        ''')

        # Load initial data
        load_customers_data(cursor)
        load_items_data(cursor)

        conn.commit()
    print("Database initialized successfully.")

def load_customers_data(cursor):
    try:
        with open('customers.json', 'r') as file:
            customers = json.load(file)
        for phone, name in customers.items():
            cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, f"{phone}@example.com"))
    except FileNotFoundError:
        print("Error: customers.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in customers.json.")

def load_items_data(cursor):
    try:
        with open('items.json', 'r') as file:
            items = json.load(file)
        for item_name, details in items.items():
            cursor.execute('INSERT INTO items (name, description, price) VALUES (?, ?, ?)', (item_name, '', details['price']))
    except FileNotFoundError:
        print("Error: items.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in items.json.")

if __name__ == "__main__":
    initialize_database()
