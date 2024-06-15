import pandas as pd
import sqlite3
import os
db_file = 'bikestore.db'


if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Deleted existing database file: {db_file}")
else:
    print(f"No existing database file found: {db_file}")

database = sqlite3.connect('bikestore.db')
cursor = database.cursor()



csv = '/Users/huanghejun/Downloads/archive (1)/categories.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS categories
''')
cursor.execute('''
CREATE TABLE categories(
    category_id TEXT PRIMARY KEY,
    category_name TEXT
)
''')
database.commit()
data_flow.to_sql('categories', database, if_exists='replace', index=False)
print("成功存入categories")

#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/brands.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS brands
''')
cursor.execute('''
CREATE TABLE brands(
    brand_id TEXT,
    brand_name TEXT
)
''')
database.commit()
data_flow.to_sql('brands', database, if_exists='replace', index=False)
print("成功存入brands")

#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/products.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS products
''')
cursor.execute('''
CREATE TABLE products(
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    brand_id TEXT,
    category_id TEXT,
    model_year TEXT,
    list_price REAL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
)
''')
database.commit()
data_flow.to_sql('products', database, if_exists='replace', index=False)
print("成功存入products")

#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/stocks.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS stocks
''')
cursor.execute('''
CREATE TABLE stocks(
    store_id TEXT,
    product_id TEXT,
    quantity TEXT,
    PRIMARY KEY(store_id,product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')
database.commit()
data_flow.to_sql('stocks', database, if_exists='replace', index=False)
print("成功存入stocks")
cursor.execute("SELECT * from stocks")
#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/order_items.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS order_items
''')
cursor.execute('''
CREATE TABLE order_items(
    order_id TEXT,
    item_id TEXT,
    product_id TEXT,
    quantity TEXT,
    list_price TEXT,
    discount TEXT,
    PRIMARY KEY (order_id, item_id)    
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')
database.commit()
data_flow.to_sql('order_items', database, if_exists='replace', index=False)
print("成功存入order_items")
#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/stores.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS stores
''')
cursor.execute('''
CREATE TABLE stores (
    store_id TEXT PRIMARY KEY,
    store_name TEXT,
    phone TEXT,
    email TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    FOREIGN KEY (store_id) REFERENCES stocks(store_id)
)
''')
database.commit()
data_flow.to_sql('stores', database, if_exists='replace', index=False)
print("成功存入stores")
#///////////////////////////////////////////////////////////////////////



csv = '/Users/huanghejun/Downloads/archive (1)/staffs.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS staffs
''')
cursor.execute('''
CREATE TABLE staffs (
    staff_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,       
    email TEXT,
    phone TEXT,
    active TEXT,
    store_id TEXT,
    manager_id TEXT,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (manager_id) REFERENCES staffs(staff_id)
)
''')
database.commit()
data_flow.to_sql('staffs', database, if_exists='replace', index=False)
print("成功存入staffs")

# #///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/customers.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS customers
''')
cursor.execute('''
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,       
    phone TEXT,
    email TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
)
''')
database.commit()
data_flow.to_sql('customers', database, if_exists='replace', index=False)
print("成功存入customer")
#///////////////////////////////////////////////////////////////////////


csv = '/Users/huanghejun/Downloads/archive (1)/orders.csv'
data_flow = pd.read_csv(csv)

cursor.execute('''
DROP TABLE IF EXISTS orders
''')
cursor.execute('''
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_status TEXT,
    order_date TEXT
    required_date TEXT    
    shipped_date TEXT,
    store_id TEXT,
    staff_id TEXT,
    FOREIGN KEY (staff_id) REFERENCES staffs(staff_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (order_id) REFERENCES order_items(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

database.commit()
data_flow.to_sql('orders', database, if_exists='replace', index=False)
print("成功存入orders")


database.close()

