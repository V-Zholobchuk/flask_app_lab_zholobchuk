# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from .models import PostCategory
from datetime import datetime, UTC 

class PostForm(FlaskForm):
    title = StringField("Title", 
                        validators=[DataRequired(), Length(min=2, max=150)])
    
    content = TextAreaField("Content", 
                            validators=[DataRequired()], 
                            render_kw={"rows": 5})
    
    is_active = BooleanField('Active Post', default=True)
    
    publish_date = DateTimeLocalField('Publish Date', 
                                      format="%Y-%m-%dT%H:%M", 
                                      default=lambda: datetime.now(UTC)) 
    
    category = SelectField('Category', 
                           choices=[(cat.name, cat.value) for cat in PostCategory], 
                           validators=[DataRequired()])
    
    submit = SubmitField("Submit")