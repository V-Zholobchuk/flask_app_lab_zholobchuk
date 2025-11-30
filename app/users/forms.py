from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.users.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=4, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Таке ім\'я вже зайняте.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=4, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    about_me = TextAreaField('About Me', validators=[Length(max=140)])
    
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'])
    ])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Таке ім\'я вже зайняте.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email вже зареєстрований.')
            
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    
    password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=6)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    
    submit = SubmitField('Change Password')            