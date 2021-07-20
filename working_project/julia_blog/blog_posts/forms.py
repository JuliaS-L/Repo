
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    blog_title = StringField('Title',validators=[DataRequired()])
    blog_text = TextAreaField('Text',validators=[DataRequired])
    submit = SubmitField('Create')
