from app import app 
from flask import render_template, url_for, request, flash, redirect
from .forms import ContactForm 
from .logger import contact_logger

@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data

        contact_logger.info(f"New contact form submission: Name={name}, Email={email}, Phone={phone}, Message={message}")

        flash(f'Повідомлення від {name} ({email}) успішно відправлено!', 'success')

        return redirect(url_for('contacts'))

    return render_template('contacts.html', title='Контакти', form=form)