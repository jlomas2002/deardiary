from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class Entry(Form):
    date = DateField('date', format='%d/%m/%Y', validators=[DataRequired()], description="dd/mm/yyyy")
    event = description = TextAreaField('event', description="What happened today?")
    feeling = TextAreaField('feeling', description="How did you feel today?")
    comments = TextAreaField('comments', description="Any further comments?")
    summ = StringField('summary', validators=[DataRequired(), Length(min=1, max=1)], description="One word summary")
    private = BooleanField('private')


class Login(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=1, max=30)])
    password = StringField('password', validators=[DataRequired(), Length(min=1, max=30)])

class Register(Form):
    fname = StringField('fname', validators=[DataRequired(), Length(min=1, max=30)])
    lname = StringField('lname', validators=[DataRequired(), Length(min=1, max=30)])
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=30)])
    password = StringField('password', validators=[DataRequired(), Length(min=5, max=30)])

class UserSearch(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=30)], description="username")

class ChangePW(Form):
    old =  password = StringField('old', validators=[DataRequired()])
    new =  password = StringField('old', validators=[DataRequired()])