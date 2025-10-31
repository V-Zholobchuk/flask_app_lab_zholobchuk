from flask import Flask

app = Flask(__name__) 
app.config["SECRET_KEY"] = "a-very-secret-and-random-key-12345" 

from . import views 

from .users import users_bp
app.register_blueprint(users_bp)

from .products import products_bp
app.register_blueprint(products_bp,url_prefix='/products')
