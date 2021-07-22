#crud
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    project_title = StringField('Title',[validators.DataRequired()])
    project_description = TextAreaField('Short Description',[validators.DataRequired()])
    project_text = TextAreaField('Text',[validators.DataRequired()])
    project_code = TextAreaField('Code',[validators.DataRequired()])
    project_github_code = TextAreaField('Github Url')
    project_trinket_code = TextAreaField('Trinket Url')
    submit = SubmitField('Create')
#Image??
