from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, length, EqualTo

class UserForm(FlaskForm):
    name = StringField(label="Enter your name", validators=[DataRequired(),length(min=3,max=100)])
    email = StringField(label="Enter your email", validators=[DataRequired(),length(min=3,max=60)])
    password = PasswordField(label="Enter a password", validators=[DataRequired(), length(min=5,max=30), EqualTo("password_test")])
    password_test = PasswordField(label="Enter the same password",validators=[DataRequired(),length(min=5,max=30)])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField(label="Enter your email", validators=[DataRequired(),length(min=3,max=60)])
    password = PasswordField(label="Enter a password", validators=[DataRequired(), length(min=5,max=30)])
    submit = SubmitField()

class UserPostForm(FlaskForm):
    title = StringField(label="Title",validators=[DataRequired(),length(min=2,max=30)])
    author = StringField(label="Author",validators=[DataRequired(),length(min=2,max=30)])
    slug =  StringField(label="Slug",validators=[DataRequired(),length(min=2,max=30)])
    content = TextAreaField(label="Content", validators=[DataRequired(), length(min=1)])
    submit = SubmitField()