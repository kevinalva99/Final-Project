from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel): 
    customer_id: int 
    name: str
    phone: str

class Item(BaseModel):
    item_id: int
    name: str
    price: float

class Order(BaseModel):
    order_id: int 
    timestamp: int
    cust_id: int
    notes: str

app = FastAPI()

def db_setup():
    con = sqlite3.connect("db.sqlite")
    con.row_factory = sqlite3.Row  # Enable dict-like access to rows
    cur = con.cursor()
    return con, cur

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    con, cur = db_setup()
    cur.execute("SELECT * FROM customers WHERE id=?;", (customer_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(row)

@app.delete("/customers/{customer_id}")
def del_customer(customer_id: int):
    con, cur = db_setup()
    cur.execute("DELETE FROM customers WHERE id=?;", (customer_id,))
    con.commit()
    return {"rows_affected": cur.rowcount}

@app.put("/customers/")
def update_customer(customer: Customer):
    con, cur = db_setup()
    cur.execute(
        "UPDATE customers SET name=?, phone=? WHERE id=?;", 
        (customer.name, customer.phone, customer.customer_id)
    )
    con.commit()
    return {"rows_affected": cur.rowcount}

@app.post("/customers/")
def create_customer(customer: Customer):
    con, cur = db_setup()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    con.commit()
    return {"id": cur.lastrowid, "name": customer.name, "phone": customer.phone}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    con, cur = db_setup()
    cur.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)

@app.delete("/items/{item_id}")
def del_item(item_id: int):
    con, cur = db_setup()
    cur.execute("DELETE FROM items WHERE id=?;", (item_id,))
    con.commit()
    return {"rows_affected": cur.rowcount}

@app.put("/items/")
def update_item(item: Item):
    con, cur = db_setup()
    cur.execute(
        "UPDATE items SET name=?, price=? WHERE id=?;", 
        (item.name, item.price, item.item_id)
    )
    con.commit()
    return {"rows_affected": cur.rowcount}

@app.post("/items/")
def create_item(item: Item):
    con, cur = db_setup()
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    con.commit()
    return {"id": cur.lastrowid, "name": item.name, "price": item.price}

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    con, cur = db_setup()
    cur.execute("SELECT * FROM orders WHERE id=?;", (order_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(row)

@app.delete("/orders/{order_id}")
def del_order(order_id: int):
    con, cur = db_setup()
    cur.execute("DELETE FROM orders WHERE id=?;", (order_id,))
    con.commit()
    return {"rows_affected": cur.rowcount}

@app.put("/orders/")
def update_order(order: Order):
    con, cur = db_setup()
    timestamp = int(datetime.now().timestamp())
    if order.cust_id == 0:
        res = cur.execute("SELECT cust_id FROM orders WHERE id = ?;", (order.order_id,))
        current_cust_id = res.fetchone()
        cust_id = current_cust_id[0]
    else:
        cust_id = order.cust_id
    cur.execute(
        "UPDATE orders SET timestamp = ?, notes = ?, cust_id = ? WHERE id = ?;",
        (timestamp, order.notes, cust_id, order.order_id)
    )
    con.commit()


@app.post("/orders/")
def create_order(order: Order):
    con, cur = db_setup()

    cur.execute("SELECT id FROM customers WHERE id = ?;", (order.cust_id,))
    existing_customer = cur.fetchone()

    if not existing_customer:
        cur.execute(
            "INSERT INTO customers (name, phone) VALUES (?, ?);",
            ("New Customer", "000-000-0000")  
        )
        con.commit()
        new_cust_id = cur.lastrowid
    else:
        new_cust_id = order.cust_id

    cur.execute("SELECT MAX(id) FROM orders;")
    last_order_id = cur.fetchone()[0] or 0
    new_order_id = last_order_id + 1

    timestamp = int(datetime.now().timestamp())

    cur.execute(
        "INSERT INTO orders (id, timestamp, cust_id, notes) VALUES (?, ?, ?, ?);",
        (new_order_id, timestamp, new_cust_id, order.notes)
    )
    con.commit()

    return {
        "order_id": new_order_id,
        "timestamp": timestamp,
        "cust_id": new_cust_id,
        "notes": order.notes
    }
