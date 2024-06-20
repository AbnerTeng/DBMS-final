import os
from flask import Flask, request, render_template, g
import shutil
import sqlite3
import csv
from .constants import (
    CSV_FILES, QUERY_1, QUERY_2, QUERY_5, QUERY_6
)
from .utils import tup2list, execute_sql_file

current_dir = os.path.dirname(os.path.realpath(__file__))

# 根據提供的目錄結構設置模板和靜態文件夾
static_folder = os.path.join(current_dir, '../frontend/static')
template_folder = os.path.join(current_dir, '../frontend/templates')

# 打印路径用于调试
print(f"Static folder: {static_folder}")
print(f"Template folder: {template_folder}")

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

# 全局變量
id = 1616

initial_db_path = os.path.join(current_dir, 'bike.db')
database = os.path.join(current_dir, 'bikestore.db')

# 将初始数据库文件复制到工作目录中
def reset_database():
    if os.path.exists(database):
        os.remove(database)
    shutil.copyfile(initial_db_path, database)

# 在应用启动时重置数据库
reset_database()


def get_db_connection():
    conn = sqlite3.connect(database)
    return conn

@app.before_request
def before_request():
    g.db = get_db_connection()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def show1():
    return render_template('index.html')

@app.route("/new")
def show2():
    return render_template('new.html')

@app.route("/new_tackle", methods=["POST"])
def new():
    global id
    
    customer_id = request.form['customer_id']
    order_status = request.form['order_status']
    order_date = request.form['order_date']
    required_date = request.form['required_date']
    shipped_date = request.form['shipped_date']
    store_id = request.form['store_id']
    staff_id = request.form['staff_id']
    item_id = 1
    products_id = request.form['product_id']
    quantities = request.form['quantity'] 
    discount = request.form['discount']
    
    cursor = g.db.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?;", (customer_id,))
    customer_search = cursor.fetchone()
    if customer_search == None:
        result = "您的帳號不存在，請先創建帳戶再進行訂購"
        return render_template('result.html', result=result)
    
    product_id = products_id.split(',')
    quantity = quantities.split(',')
    arr = []
    cost = 0
    
    for i in range(len(product_id)):
        cursor.execute("SELECT product_id, quantity FROM stocks WHERE product_id = ? AND store_id = ?;", (product_id[i], store_id))
        stock_quantity = int(cursor.fetchone()[1])
        if stock_quantity >= int(quantity[i]):
            arr.append(product_id[i])
            remain_quantity = stock_quantity - int(quantity[i])
            cursor.execute("UPDATE stocks SET quantity = ? WHERE product_id = ? AND store_id = ?;", (str(remain_quantity), product_id[i], store_id))
            cursor.execute("SELECT list_price FROM products WHERE product_id = ?;", (product_id[i],))
            list_price = float(cursor.fetchone()[0])
            cost += int(quantity[i]) * list_price
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (?, ?, ?, ?, ?, ?);", 
                (str(id), str(item_id), str(product_id[i]), quantity[i], list_price, discount)
            )
            item_id += 1
    
    if len(arr) > 0:
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", 
            (id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id)
        )
        id += 1
        g.db.commit()
        cost = cost * float(discount)
        result = f"您購物車裡id = {arr} 商品新增成功, 總共{cost}元"
    else:
        result = '存貨不足，您的訂單新增失敗！'
    
    return render_template('result.html', result=result)

@app.route("/delete")
def show3():
    return render_template('delete.html')

@app.route("/delete_tackle", methods=["POST"])
def delete():
    delete_id = request.form['order_id']
    cursor = g.db.cursor()
    cursor.execute("SELECT order_id FROM orders WHERE order_id = ?;", (delete_id,))
    data = cursor.fetchone()
    result = '找不到您的訂單，無法進行刪除'
    if data is None:
        return render_template('result.html', result=result)
    else:
        cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id = ?;", (delete_id,))
        order_quantity = cursor.fetchall()
        for product, quantity in order_quantity:
            cursor.execute("SELECT quantity FROM stocks WHERE product_id = ?;", (product,))
            remain_quantity = cursor.fetchone()[0]
            cursor.execute("UPDATE stocks SET quantity = ? WHERE product_id = ?;", (remain_quantity + quantity, product))
        cursor.execute("DELETE FROM orders WHERE order_id = ?;", (delete_id,))
        cursor.execute("DELETE FROM order_items WHERE order_id = ?;", (delete_id,))
        result = "您的訂單已刪除完成"
        return render_template("result.html", result=result)

# 新增更新訂單的路由
@app.route("/update")
def show4():
    return render_template('update.html')

@app.route("/update_tackle", methods=["POST"])
def update():
    order_id = request.form['order_id']
    customer_id = request.form['customer_id']
    order_status = request.form['order_status']
    order_date = request.form['order_date']
    required_date = request.form['required_date']
    shipped_date = request.form['shipped_date']
    store_id = request.form['store_id']
    staff_id = request.form['staff_id']
    
    cursor = g.db.cursor()
    cursor.execute("SELECT order_id FROM orders WHERE order_id = ?;", (order_id,))
    order_search = cursor.fetchone()
    if order_search is None:
        result = "找不到您的訂單，無法進行更新"
        return render_template('result.html', result=result)

    cursor.execute(
        "UPDATE orders SET customer_id = ?, order_status = ?, order_date = ?, required_date = ?, shipped_date = ?, store_id = ?, staff_id = ? WHERE order_id = ?;",
        (customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id, order_id)
    )
    g.db.commit()
    result = f"訂單 {order_id} 已成功更新"
    
    return render_template('result.html', result=result)

@app.route("/update_order_item")
def show_update_order_item():
    return render_template('update_order_item.html')

@app.route("/update_order_item_tackle", methods=["POST"])
def update_order_item():
    order_id = request.form['order_id']
    item_id = request.form['item_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    list_price = request.form['list_price']
    discount = request.form['discount']

    cursor = g.db.cursor()
    cursor.execute("SELECT order_id, item_id FROM order_items WHERE order_id = ? AND item_id = ?;", (order_id, item_id))
    order_item_search = cursor.fetchone()
    if order_item_search is None:
        result = "找不到您的訂單項目，無法進行更新"
        return render_template('result.html', result=result)

    cursor.execute(
        "UPDATE order_items SET product_id = ?, quantity = ?, list_price = ?, discount = ? WHERE order_id = ? AND item_id = ?;",
        (product_id, quantity, list_price, discount, order_id, item_id)
    )
    g.db.commit()
    result = f"訂單項目 {order_id}-{item_id} 已成功更新"
    
    return render_template('result.html', result=result)

###
@app.route('/dashboard')
def dashboard() -> render_template:
    """
    Query datas to show on the dashboard
    """
    conn = sqlite3.connect(database)
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

@app.route("/search")
def show_search_order_item():
    return render_template('search.html')

@app.route('/search_bycustomerID', methods=['GET', 'POST'])
def orders():
    """
    Get orders by customer ID
    """
    msg = "msg"
    if request.method == "POST":
        con = sqlite3.connect(database)

        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        customer_id = int(request.form.get("search_order"))
        print(f"Searching for customer_id: {customer_id}")
        cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        _orders = cursor.fetchall()

        if _orders:
            msg = "查詢結果如下！"
            return render_template("result_customerID.html", order_search=_orders, msg=msg)

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
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # cur = conn.cursor()
    cur.execute("SELECT * FROM staffs WHERE manager_id = 1")
    staff= cur.fetchall()
    return render_template("search_manager.html", staff_search=staff)

@app.route("/search_sales")
def sales():
    """
    Get sales by month and category
    """
    con = sqlite3.connect(database)
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
###

if __name__ == "__main__":
    app.run(debug=True)
