from . import post_bp
from app import db
from .models import Post,Tag
from .forms import PostForm
from flask import render_template, redirect, url_for, flash, session, abort, request
from flask_wtf import FlaskForm 
from app.users.models import User

def populate_form_choices(form):
    authors = db.session.scalars(db.select(User).order_by(User.username)).all()
    form.author_id.choices = [(a.id, a.username) for a in authors]
    
    tags = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()
    form.tags.choices = [(t.id, t.name) for t in tags]
    
    return form

@post_bp.route('/create', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    form = populate_form_choices(form) 
    
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data
        )
        
        selected_ids = form.tags.data
        tags_objects = db.session.scalars(db.select(Tag).where(Tag.id.in_(selected_ids))).all()
        new_post.tags = tags_objects

        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", 'success')
        return redirect(url_for('.get_posts')) 
    
    return render_template('add_post.html', form=form, title="Створити Новий Пост")

@post_bp.route('/')
def get_posts():
    
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    
    return render_template('posts.html', posts=posts)



@post_bp.route('/<int:id>')
def detail_post(id):
    
    post = db.get_or_404(Post, id)
    
    return render_template('detail_post.html', post=post)

from flask import render_template, redirect, url_for, flash, session, abort, request
from .forms import PostForm
from flask_wtf import FlaskForm 


@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form = populate_form_choices(form)

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [t.id for t in post.tags]
    
    if form.validate_on_submit():
        
        
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.user_id = form.author_id.data

        
        post.tags.clear()
        selected_ids = form.tags.data
        tags_objects = db.session.scalars(db.select(Tag).where(Tag.id.in_(selected_ids))).all()
        post.tags.extend(tags_objects)

        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("add_post.html", form=form, title="Редагувати пост")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    form = FlaskForm() 
    
    if request.method == 'POST':
        
        
        db.session.delete(post) 
        db.session.commit() 
        flash("Пост успішно видалено", "danger") 
        return redirect(url_for('.get_posts')) 

    return render_template('delete_confirm.html', post=post, form=form) 