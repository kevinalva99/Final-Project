import sqlite3
import json

connection = sqlite3.connect("dosa.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
	id INTEGER PRIMARY KEY,
	name CHAR(64) NOT NULL,
	phone CHAR(10) NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
	id INTEGER PRIMARY KEY,
	name CHAR(64) NOT NULL,
	price REAL NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
	id INTEGER PRIMARY KEY,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	cust_id INT NOT NULL,
    notes TEXT
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list(
    order_id NOT NULL,
    item_id NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

def add_customer(name, phone):
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);",
                   (name, phone))

def list_customers():
    rows = cursor.execute("SELECT id, name, phone FROM customers;").fetchall()
    return rows

def print_customers():
    for customer in list_customers():
        print(f"ID: {customer[0]} Name: {customer[1]} Phone: {customer[2]}")
    
def count_customers():
    rows = cursor.execute("SELECT COUNT(*) FROM customers;").fetchone()
    return rows[0]

with open('example_orders.json', 'r') as filename:
    data = json.load(filename)

customers = {}

for order in data:
    name = order['name']
    phone = order['phone']
    customers[phone] = name

for (phone, name) in customers.items():
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

items = {}

for order in data:
    for item in order['items']:
        name = item['name']
        price = item['price']
        items[name] = price
for (name, price) in items.items():
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))

for order in data:
    phone = order['phone']
    timestamp = order['timestamp']
    notes = order['notes']
    res = cursor.execute("SELECT id FROM customers WHERE phone=?;", (phone,))
    cust_id = res.fetchone()[0]
    cursor.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);", (timestamp, cust_id, notes))
    order_id = cursor.lastrowid
    for item in order['items']:
        item_name = item['name']
        res = cursor.execute("SELECT id FROM items WHERE name=?;", (item_name,))
        item_id = res.fetchone()[0]
        cursor.execute("INSERT INTO item_list(order_id,item_id) VALUES(?, ?);", (order_id, item_id))
    
    

connection.commit()