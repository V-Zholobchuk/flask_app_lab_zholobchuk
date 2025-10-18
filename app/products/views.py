from . import products_bp
from flask import render_template

example_products = [
    {"id": 1, "name": "Ноутбук", "price": 1500},
    {"id": 2, "name": "Миша", "price": 50},
    {"id": 3, "name": "Клавіатура", "price": 100}
]

@products_bp.route('/')
def product_list():
    return render_template('products/product_list.html', 
                           title="Список товарів", 
                           products=example_products)