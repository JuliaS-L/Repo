#used for submit questions
#crud
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    contact_text = TextAreaField('Text',validators=[DataRequired])
    submit = SubmitField('Send')
#Image??
