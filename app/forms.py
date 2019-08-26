from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PostNewsArticle(FlaskForm):
    heading = TextAreaField(u'Write heading', validators=[
        DataRequired(), Length(min=1)])
    post = TextAreaField(u'Write news', validators=[
        DataRequired(), Length(min=1)])
    submit = SubmitField('Submit News')

class CreateNewHuman(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    full_name = StringField('Full name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Telephone')
    links = StringField('Links')
    ##ids = StringField('IDs')
    orcid = StringField('ORCID')
    researcher_id = StringField('Reasearcher id')
    scopus_id = StringField('SCOPUS id')
    submit = SubmitField('Create Human')
