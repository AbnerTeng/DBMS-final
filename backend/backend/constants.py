"""
constants
"""
CSV_FILES = {
    'stores': 'stores.csv',
    'staffs': 'staffs.csv',
    'categories': 'categories.csv',
    'brands': 'brands.csv',
    'products': 'products.csv',
    'customers': 'customers.csv',
    'orders': 'orders.csv',
    'order_items': 'order_items.csv',
    'stocks': 'stocks.csv'
}

QUERY_1 = """
SELECT COUNT(customer_id) AS total_customers
FROM customers
"""

QUERY_2 = """
SELECT COUNT(order_id) AS total_orders
FROM order_items
"""

QUERY_3 = """
SELECT DISTINCT(category_name) AS categories
FROM categories
"""

QUERY_4 = """
SELECT DISTINCT(brand_name) AS brands
FROM brands 
"""

QUERY_5 = """
SELECT 
    COUNT(oi.order_id) AS num_orders,
    c.category_name AS category_name
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
"""

QUERY_6 = """
SELECT
    COUNT(oi.order_id) AS num_orders,
    b.brand_name AS brand_name
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN brands b
    ON p.brand_id = b.brand_id
GROUP BY b.brand_name
"""