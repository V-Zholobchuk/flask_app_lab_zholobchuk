from app import app 
from flask import render_template, url_for 

@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти')