from flask import Flask, render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config 
from sqlalchemy import MetaData 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
bcrypt = Bcrypt() 
login_manager = LoginManager() 
login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    """
    Фабрика, що створює та конфігурує екземпляр додатку Flask.
    """
    app = Flask(__name__, 
                instance_relative_config=True,
                static_folder='static',
                template_folder='templates')

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db) 
    bcrypt.init_app(app) 
    login_manager.init_app(app)
    
    from .users import users_bp
    app.register_blueprint(users_bp)
    
    from .products import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix='/post') 

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404 

    @app.route('/')
    def resume():
         return render_template('resume.html', title='Резюме')

    @app.route('/contacts', methods=['GET', 'POST'])
    def contacts():
         from .forms import ContactForm
         from .logger import contact_logger
         form = ContactForm()
         if form.validate_on_submit():
             contact_logger.info("Form submitted")
             flash('Повідомлення успішно відправлено!', 'success')
             return redirect(url_for('contacts'))
         return render_template('contacts.html', title='Контакти', form=form)

    return app