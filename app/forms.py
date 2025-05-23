from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6,128)])
    submit   = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')

class NDAForm(FlaskForm):
    party_name     = StringField('Party Name', validators=[DataRequired()])
    effective_date = DateField('Effective Date', validators=[DataRequired()])
    submit         = SubmitField('Generate NDA')

class RentForm(FlaskForm):
    landlord   = StringField('Landlord Name', validators=[DataRequired()])
    tenant     = StringField('Tenant Name', validators=[DataRequired()])
    start_date = DateField('Lease Start Date', validators=[DataRequired()])
    submit     = SubmitField('Generate Rent Agreement')

class TemplateCreateForm(FlaskForm):
    name      = StringField('Template Name', validators=[DataRequired()])
    slug      = StringField('Slug (e.g. nda)', validators=[DataRequired()])
    category  = StringField('Category', validators=[DataRequired()],description="E.g. NDA, Rent Agreement…")
    region    = StringField('Region (optional)', description="E.g. India, USA…")

    docx_file = FileField('DOCX Template', validators=[DataRequired(), FileAllowed(['docx'], 'DOCX only!')])
    txt_file  = FileField('TXT Template', validators=[FileAllowed(['txt'], 'TXT only!')])
    html_file = FileField('HTML Snippet (optional)', validators=[FileAllowed(['html','htm'], 'HTML only!')])
    submit    = SubmitField('Create Template')

