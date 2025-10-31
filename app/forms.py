from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[
        DataRequired(), 
        Length(min=4, max=10, message="Ім'я має бути від 4 до 10 символів")
    ]) 
    
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message="Некоректний email")
    ]) 
    
    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX")
    ]) 
    
    subject = SelectField('Тема', choices=[
        ('1', 'Загальне питання'),
        ('2', 'Технічна підтримка'),
        ('3', 'Партнерство')
    ], validators=[DataRequired()]) 
    
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(), 
        Length(max=500, message="Повідомлення не може перевищувати 500 символів")
    ]) 
    
    submit = SubmitField('Відправити') 


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Це поле обов'язкове")
    ]) 
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ]) 
    
    remember = BooleanField("Запам'ятай мене") 
    
    submit = SubmitField('Sign In') 