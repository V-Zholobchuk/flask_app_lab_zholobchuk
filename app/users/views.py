from flask import request, redirect, url_for, render_template
from . import users_bp 

@users_bp.route("/hi/<string:name>") 
def greetings(name): 
    age = request.args.get("age", None, int) 
    
    return render_template("users/hi.html",
                           name=name.upper(), age=age) 

@users_bp.route("/admin") 
def admin(): 
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True) #
    print(to_url)
    return redirect(to_url) 