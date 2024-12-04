from fastapi import FastAPI
import sqlite3
from pydantic import Basemodel
from datetime import datetime

class Customer(BaseModel): 
  customer_id: int
  name: str
  id: str

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
    return(con, con.cursor())
  
@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
  cur = db_setup()
  res = cur.execute("SELECT * FROM customers WHERE id=?;", (customer_id,))
  row = res.fetchone()
  return{
    "id": row[0],
    "name": row[1],
    "phone": row[2],
  }

@app.delete("/customers/{customer_id}")
def del_customer(customer_id: int):
  cur = db_setup()
  res = cur.execute("DELETE FROM customers WHERE id=?;", (customer_id,))
  return("rows_affected", cur.rowcount)

@app.put("/customers/")
def update_customer(customer: Customer):
  cur, conn = db_setup
  res = cur.execute("UPDATE customers SET name=?, phone=?, WHERE id=?;", (customer.name, customer.phone, customer.customer_id))
  return("rows_affected",)

@app.post("/customers/")
def creat_customer(customer: Customer):
  cur = db_setup()
  res = cur.execute("INSERT INTO customers (name, phone) VALUES(?, ?);", (customer.name, customer.phone))
  customer_id = res.lastrowid
  return{
    "id": customer_id,
    "name": customer.name,
    "phone": customer.phone,
  }

@app.get("/items/{item_id}")
def read_items(item_id: int):
  cur = db_setup()
  res = cur.execute("SELECT * FROM items WHERE id=?;", (item_id,))
  row = res.fetchone()
  return{
    "id": row[0],
    "name": row[1],
    "phone": row[2],
  }

@app.delete("/items/{item_id}")
def del_items(item_id: int):
  cur = db_setup()
  res = cur.execute("DELETE FROM items WHERE id=?;", (item_id,))
  return("rows_affected", cur.rowcount)

@app.put("/items/")
def update_item(item: Item):
  cur, conn = db_setup
  res = cur.execute("UPDATE items SET name=?, price=?, WHERE id=?;", (item.name, item.phone, item.item_id))
  return("rows_affected",)

@app.post("/items/")
def creat_customer(item: Item):
  cur = db_setup()
  res = cur.execute("INSERT INTO items (name, phone) VALUES(?, ?);", (item.name, item.phone))
  item_id = res.lastrowid
  return{
    "id": item_id,
    "name": item.name,
    "price": item.price,
  }
