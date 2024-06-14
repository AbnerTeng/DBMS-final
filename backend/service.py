from flask import Flask, request, render_template, g
import sqlite3
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

static_folder = os.path.join(current_dir, '../frontend/static')
template_folder = os.path.join(current_dir, '../frontend/templates')

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

id = 1616
database = os.path.join(current_dir, 'bikestore.db')

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
    
    product_id = products_id.split(',')
    quantity = quantities.split(',')
    arr =[]
    cost = 0
    for i in range(len(product_id)):
        cursor.execute("SELECT product_id,quantity FROM stocks WHERE product_id = ? AND store_id = ?;", (product_id[i],store_id))
        stock_quantity = int(cursor.fetchone()[1])
        if stock_quantity >= int(quantity[i]):
            arr.append(product_id[i])
            remain_quantity = stock_quantity - int(quantity[i])
            cursor.execute("UPDATE stocks SET quantity = ? WHERE product_id = ?;", (str(remain_quantity), product_id[i]))
            cursor.execute("SELECT list_price from products WHERE product_id = ?;",(product_id[i],))     
            list_price = float(cursor.fetchone()[0])
            cost +=  int(quantity[i]) * list_price
            cursor.execute(
            "INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (?, ?, ?, ?, ?, ?);", 
            (str(id),str(item_id), str(product_id[i]), quantity[i], list_price,discount)
             )
            item_id +=1
    
    if(len(arr) >0):
             cursor.execute(
            "INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", 
            (id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id)
             )
             id += 1
             g.db.commit()
             cost = cost * float(discount)
             result = f"您購物車裡id = {arr} 商品新增成功,總共{cost}元"
    else:
        result = '存貨不足，您的訂單新增失敗！'      
                 
    return render_template('result.html', result=result)

@app.route("/delete")
def show3():
    return render_template('delete.html')

@app.route("/delete_tackle",methods=["POST"])
def delete():
    delete_id = request.form['order_id']
    cursor = g.db.cursor()
    cursor.execute("SELECT order_id FROM orders WHERE order_id = ?;", (delete_id,))
    data = cursor.fetchone()
    result = '找不到您的訂單，無法進行刪除'
    if data == None:
        return render_template('result.html',result = result)
    else:
        cursor.execute("SELECT product_id,quantity FROM order_items WHERE order_id = ?;", (delete_id,))
        order_quantity = cursor.fetchall()
        for product,quantity in order_quantity:
            cursor.execute("SELECT quantity FROM stocks WHERE product_id = ?;", (product,))
            remain_quantity = cursor.fetchone()[0]
            cursor.execute("UPDATE stocks SET quantity = ? WHERE product_id = ?;", (remain_quantity+quantity, product))
        cursor.execute("DELETE FROM orders WHERE order_id = ?;", (delete_id,))
        cursor.execute("DELETE FROM order_items WHERE order_id = ?;", (delete_id,))
        result = "您的訂單已刪除完成"
        return render_template("result.html",result = result)
       



if __name__ == "__main__":
    app.run(port=3000)