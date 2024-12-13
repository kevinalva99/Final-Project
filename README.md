# Final-Project

init_db.py created a database containing the following tables; customers, items, orders, and item_list. We openened the json file and used it to add our data from the json file to the database. Through python(mainly for loops) and SQL we extracted the data and saved it in the their respected tables. 

main.py we used FastAPI and sqlite3 to create basemodels and connected our database to a browser. Here we set up methods to get, delete, put, and post. For the most we reused the same code. Except for the orders in which I though to use the customer phone number to find the cust_id and if it did not exist to create one. 
