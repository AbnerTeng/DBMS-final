"""
Query processing
"""
import os
import csv
import sqlite3
from flask import (Flask, request, render_template, g
)
from .constants import (
    CSV_FILES, QUERY_1, QUERY_2, QUERY_5, QUERY_6
)
from .utils import tup2list, execute_sql_file

app = Flask(
    __name__,
    static_folder="../frontend/static",
    template_folder="../frontend/templates"
)

@app.before_request
def before_request() -> None:
    """
    connect to the database before each request
    """
    g.db = get_db_connection()

@app.teardown_request
def teardown_request(db_conn=None) -> None:
    """
    Ensure the database connection is closed after each request
    """
    db_conn = getattr(g, "_database", None)
    if db_conn is not None:
        db_conn.close()

@app.route("/")
def index() -> render_template:
    """
    index page
    """
    return render_template("index.html")

def get_db_connection(db_path: str = "bike.db"):
    """
    Get a database connection and cursor
    """
    with app.app_context():
        if "db" not in g:
            g.db = sqlite3.connect(db_path)
            g.db.row_factory = sqlite3.Row

        return g.db, g.db.cursor()

def create_database(db_path: str = "bike.db") -> None:
    """
    Create a new database if it does not exist
    """
    if os.path.exists(db_path):
        return None

    with sqlite3.connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        execute_sql_file(cursor, "sql/schema.sql")

        for table_name, csv_file in CSV_FILES.items():
            with open(f"../data/{csv_file}", "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                next(csv_reader) ## skip the header row
                placeholders = ", ".join(['?' for _ in next(csv_reader)])
                cursor.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    csv_reader
                )

        cursor.execute("UPDATE staffs SET manager_id = NULLIF(manager_id, 'NULL')")

    return None

# def create_database(db_path: str = "bike.db"):
#     """
#     Create a new database
#     """
#     if not os.path.exists(db_path):
#         db_conn = sqlite3.connect(db_path)
#         curr_db = db_conn.cursor()

#         # drop table if exists
#         for table in TABLE:
#             cmd = "DROP TABLE IF EXISTS " + table
#             curr_db.execute(cmd)

#         # table stores
#         cmd = "CREATE TABLE stores (\
#             store_id INT IDENTITY (1, 1) PRIMARY KEY,\
#             store_name VARCHAR (255) NOT NULL,\
#             phone VARCHAR (25),\
#             email VARCHAR (255),\
#             street VARCHAR (255),\
#             city VARCHAR (255),\
#             state VARCHAR (10),\
#             zip_code VARCHAR (5))"
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO stores VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
#                     csv.reader(open("C:/Users/user/Downloads/Bike/stores.csv",'r', encoding='utf-8')))
#         cmd = "DELETE FROM stores WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table staffs
#         cmd = """CREATE TABLE staffs (
#         staff_id INT IDENTITY (1, 1) PRIMARY KEY,
#         first_name VARCHAR (50) NOT NULL,
#         last_name VARCHAR (50) NOT NULL,
#         email VARCHAR (255) NOT NULL UNIQUE,
#         phone VARCHAR (25),
#         active tinyint NOT NULL,
#         store_id INT NOT NULL,
#         manager_id INT,
#         FOREIGN KEY (store_id) 
#             REFERENCES stores (store_id) 
#             ON DELETE CASCADE ON UPDATE CASCADE,
#         FOREIGN KEY (manager_id) 
#             REFERENCES staffs (staff_id) 
#             ON DELETE NO ACTION ON UPDATE NO ACTION
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO staffs VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
#                     csv.reader(open("C:/Users/user/Downloads/Bike/staffs.csv", 'r', encoding='utf-8')))
#         cmd = "DELETE FROM staffs WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table categories
#         cmd = """CREATE TABLE categories (
#             category_id INT IDENTITY (1, 1) PRIMARY KEY,
#             category_name VARCHAR (255) NOT NULL
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO categories VALUES (?, ?)', 
#                         csv.reader(open("C:/Users/user/Downloads/Bike/categories.csv", 'r', encoding='utf-8')))
#         cmd = "DELETE FROM categories WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table brands
#         cmd = """CREATE TABLE brands (
#             brand_id INT IDENTITY (1, 1) PRIMARY KEY,
#             brand_name VARCHAR (255) NOT NULL
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO brands VALUES (?, ?)', 
#                         csv.reader(open("C:/Users/user/Downloads/Bike/brands.csv", 'r', encoding='utf-8')))
#         cmd = "DELETE FROM brands WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table products
#         cmd = """CREATE TABLE products (
#             product_id INT IDENTITY (1, 1) PRIMARY KEY,
#             product_name VARCHAR (255) NOT NULL,
#             brand_id INT NOT NULL,
#             category_id INT NOT NULL,
#             model_year SMALLINT NOT NULL,
#             list_price DECIMAL (10, 2) NOT NULL,
#             FOREIGN KEY (category_id) 
#                 REFERENCES categories (category_id) 
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             FOREIGN KEY (brand_id) 
#                 REFERENCES brands (brand_id) 
#                 ON DELETE CASCADE ON UPDATE CASCADE
#         )"""
#         curr_db.execute(cmd).fetchall()
#         curr_db.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', 
#                         csv.reader(open("C:/Users/user/Downloads/Bike/products.csv", 'r', encoding='utf-8')))
#         cmd = "DELETE FROM products WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table customers
#         cmd = """CREATE TABLE customers (
#             customer_id INT IDENTITY (1, 1) PRIMARY KEY,
#             first_name VARCHAR (255) NOT NULL,
#             last_name VARCHAR (255) NOT NULL,
#             phone VARCHAR (25),
#             email VARCHAR (255) NOT NULL,
#             street VARCHAR (255),
#             city VARCHAR (50),
#             state VARCHAR (25),
#             zip_code VARCHAR (5)
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
#                         csv.reader(open("C:/Users/user/Downloads/Bike/customers.csv", 'r', encoding='utf-8')))

#         cmd = "DELETE FROM customers WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table orders
#         cmd = """CREATE TABLE orders (
#             order_id INT IDENTITY (1, 1) PRIMARY KEY,
#             customer_id INT,
#             order_status tinyint NOT NULL,
#             -- Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
#             order_date DATE NOT NULL,
#             required_date DATE NOT NULL,
#             shipped_date DATE,
#             store_id INT NOT NULL,
#             staff_id INT NOT NULL,
#             FOREIGN KEY (customer_id)
#                 REFERENCES customers (customer_id)
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             FOREIGN KEY (store_id)
#                 REFERENCES stores (store_id)
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             FOREIGN KEY (staff_id)
#                 REFERENCES staffs (staff_id)
#                 ON DELETE NO ACTION ON UPDATE NO ACTION
#             )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
#                         csv.reader(open("C:/Users/user/Downloads/Bike/orders.csv", 'r', encoding='utf-8')))

#         cmd = "DELETE FROM orders WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table order_items
#         cmd = """CREATE TABLE order_items(
#             order_id INT,
#             item_id INT,
#             product_id INT NOT NULL,
#             quantity INT NOT NULL,
#             list_price DECIMAL (10, 2) NOT NULL,
#             discount DECIMAL (4, 2) NOT NULL DEFAULT 0,
#             PRIMARY KEY (order_id, item_id),
#             FOREIGN KEY (order_id)
#                 REFERENCES orders (order_id)
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             FOREIGN KEY (product_id)
#                 REFERENCES products (product_id)
#                 ON DELETE CASCADE ON UPDATE CASCADE
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany(
#             'INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)',
#             csv.reader(
#                 open(
#                     "C:/Users/user/Downloads/Bike/order_items.csv",
#                     'r',
#                     encoding='utf-8'
#                 )
#             )
#         )
#         cmd = "DELETE FROM order_items WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()

#         # table stocks
#         cmd = """CREATE TABLE stocks (
#             store_id INT,
#             product_id INT,
#             quantity INT,
#             PRIMARY KEY (store_id, product_id),
#             FOREIGN KEY (store_id) 
#                 REFERENCES stores (store_id) 
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             FOREIGN KEY (product_id) 
#                 REFERENCES products (product_id) 
#                 ON DELETE CASCADE ON UPDATE CASCADE
#         )"""
#         curr_db.execute(cmd).fetchall()

#         curr_db.executemany(
#             'INSERT INTO stocks VALUES (?, ?, ?)',
#             csv.reader(
#                 open(
#                     "C:/Users/user/Downloads/Bike/stocks.csv",
#                     'r', 
#                     encoding='utf-8'
#                 )
#             )
#         )

#         cmd = "DELETE FROM stocks WHERE rowid = 1"
#         curr_db.execute(cmd).fetchall()
#         cmd = "UPDATE staffs SET manager_id = NULLIF(manager_id, 'NULL')"
#         curr_db.execute(cmd).fetchall()

#         db_conn.commit()
#         db_conn.close()
#         # 如果数据库创建成功，返回 None
#         return None
#     else:
#         # 如果数据库已经存在，返回 None
#         return None

create_database()
db, db_cursor = get_db_connection()

@app.route('/dashboard')
def dashboard() -> render_template:
    """
    Query datas to show on the dashboard
    """
    conn = sqlite3.connect("bike.db")
    full_customers = conn.execute(QUERY_1).fetchone()[0]
    full_orders = conn.execute(QUERY_2).fetchone()[0]
    order_by_category = tup2list(
        conn.execute(QUERY_5).fetchall()
    )
    order_by_brand = tup2list(
        conn.execute(QUERY_6).fetchall()
    )
    conn.close()

    return render_template(
        "dashboard.html",
        full_customers = full_customers,
        full_orders = full_orders,
        order_by_category = order_by_category,
        order_by_brand = order_by_brand
    )

@app.route('/search_bycustomerID', methods=['GET', 'POST'])
def orders():
    """
    Get orders by customer ID
    """
    msg = "msg"
    if request.method == "POST":
        con = sqlite3.connect("bike.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        customer_id = int(request.form.get("search_order"))
        print(f"Searching for customer_id: {customer_id}")
        cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        _orders = cursor.fetchall()

        if _orders:
            msg = "Search result: "
            return render_template("result_customerID.html", order_search=orders, msg=msg)
        else:
            msg = "No results found"
            return render_template("result_customerID.html", msg=msg)
    else:
        return render_template("search_bycustomerID.html")

@app.route("/search_manager")
def manager():
    """
    Get staffs by manager ID
    """
    con = sqlite3.connect("bike.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM staffs WHERE manager_id = 1")
    staff= cur.fetchall()
    return render_template("search_manager.html", staff_search=staff)

@app.route("/search_sales")
def sales():
    """
    Get sales by month and category
    """
    con = sqlite3.connect("bike.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        """
            SELECT strftime('%m', o.order_date) AS order_month,
            p.category_id, c.category_name,
            ROUND(AVG(oi.quantity*oi.list_price*(1-oi.discount)),1) AS price
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            JOIN orders o ON oi.order_id = o.order_id 
            JOIN categories c ON c.category_id = p.category_id 
            GROUP BY order_month, p.category_id
        """
    )
    _sales = cur.fetchall()

    return render_template("search_sales.html", sales_search=_sales)


if __name__ == '__main__':
    app.run(debug=True)
    create_database()
