import os
import secrets
from datetime import datetime, timezone, timedelta 
from PIL import Image

from flask import request, redirect, url_for, render_template, session, flash, make_response, current_app
from flask_login import login_user, current_user, logout_user, login_required

from app import db, bcrypt
from . import users_bp
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,ChangePasswordForm

def save_picture(form_picture):
    """Зберігає аватарку, зменшуючи її розмір."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}! You can now log in', 'success')
        return redirect(url_for('users.login'))
        
    return render_template('users/register.html', title='Register', form=form)

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

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.get_posts')) 

    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            
            flash(f'Ви успішно увійшли як {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Вхід не вдався. Перевірте email та пароль.', 'danger')
            
    return render_template('users/login.html', title='Login', form=form)

@users_bp.route('/profile')
@login_required 
def profile():
    return render_template('users/profile.html', 
                           username=current_user.username, 
                           cookies=request.cookies)

@users_bp.route('/logout')
@login_required 
def logout():
    
    logout_user() 
    
    flash('Ви успішно вийшли з системи.', 'info')
    return redirect(url_for('users.login')) 


@users_bp.route('/add-cookie', methods=['POST'])
@login_required  
def add_cookie():    
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    expiry_days = request.form.get('expiry_days')

    resp = make_response(redirect(url_for('users.profile')))

    if key and value:
        if expiry_days:
            expires_at = datetime.datetime.now() + datetime.timedelta(days=int(expiry_days))
            resp.set_cookie(key, value, expires=expires_at)
        else:
            resp.set_cookie(key, value)
        flash(f'Кукі "{key}" додано.', 'success')
    else:
        flash('Ключ та Значення є обов\'язковими.', 'danger')

    return resp

@users_bp.route('/delete-cookie', methods=['POST'])
@login_required  
def delete_cookie():

    key = request.form.get('cookie_key_to_delete')
    resp = make_response(redirect(url_for('users.profile')))

    if key:
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено.', 'success')

    return resp

@users_bp.route('/delete-all-cookies', methods=['POST'])
@login_required  
def delete_all_cookies():
    resp = make_response(redirect(url_for('users.profile')))
    
    for key in request.cookies.keys():
        if key != 'session' and key != 'remember_token':
            resp.delete_cookie(key)

    flash('Всі кукі (окрім сесії) видалено.', 'success')
    return resp

@users_bp.route('/change-theme/<string:theme>')
@login_required  
def change_theme(theme):
    
    resp = make_response(redirect(url_for('users.profile')))

    max_age_seconds = 30 * 24 * 60 * 60 
    resp.set_cookie('theme', theme, max_age=max_age_seconds)
    
    flash(f'Тему змінено на "{theme}".', 'info')

    return resp


@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('users/account.html', title='Account', 
                           image_file=image_file, form=form)

@users_bp.route("/users")
@login_required 
def all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    
    count = len(users)
    
    return render_template('users/users.html', users=users, count=count)

@users_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
@users_bp.route("/account/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):

            
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            current_user.password = hashed_password
            db.session.commit()

            flash('Ваш пароль успішно оновлено!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Невірний поточний пароль. Спробуйте ще раз.', 'danger')

    return render_template('users/change_password.html', title='Change Password', form=form)        