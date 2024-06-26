from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, length, EqualTo

class UserForm(FlaskForm):
    name = StringField(label="Enter your name", validators=[DataRequired(),length(min=3,max=100)])
    email = StringField(label="Enter your email", validators=[DataRequired(),length(min=3,max=60)])
    password = PasswordField(label="Enter a password", validators=[DataRequired(), length(min=5,max=30), EqualTo("password_test")])
    password_test = PasswordField(label="Enter the same password",validators=[DataRequired(),length(min=5,max=30)])
    submit = SubmitField()