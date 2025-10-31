from flask import request, redirect, url_for, render_template, session, flash, make_response
from . import users_bp 
import datetime
from app.forms import LoginForm

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

@users_bp.route('/login', methods=['GET', 'POST'])
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        remember = form.remember.data  

        VALID_USERNAME = 'user1'
        VALID_PASSWORD = 'pass123'

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['username'] = username
            
            remember_message = " (з запам'ятовуванням)" if remember else ""
            flash(f'Вітаємо, {username}! Ви успішно увійшли{remember_message}.', 'success')
            
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильний логін або пароль.', 'danger') 
            return redirect(url_for('users.login'))

    
    return render_template('users/login.html', form=form)


@users_bp.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        cookies_data = request.cookies
        return render_template('users/profile.html', username=username,cookies=cookies_data) 
    else:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login')) 

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login')) 


@users_bp.route('/add-cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

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
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    key = request.form.get('cookie_key_to_delete')
    resp = make_response(redirect(url_for('users.profile')))

    if key:
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено.', 'success')

    return resp

@users_bp.route('/delete-all-cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    for key in request.cookies.keys():
        if key != 'session':
            resp.delete_cookie(key)

    flash('Всі кукі (окрім сесії) видалено.', 'success')
    return resp

@users_bp.route('/change-theme/<string:theme>')
def change_theme(theme):
    if 'username' not in session:
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))

    max_age_seconds = 30 * 24 * 60 * 60 
    resp.set_cookie('theme', theme, max_age=max_age_seconds)
    flash(f'Тему змінено на "{theme}".', 'info')

    return resp