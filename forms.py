from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, length, EqualTo

class UserForm(FlaskForm):
    name = StringField(label="Digite seu nome", validators=[DataRequired(),length(min=3,max=100)])
    username = StringField(label="Digite um username", validators=[DataRequired(),length(min=3,max=30)])
    email = StringField(label="Digite seu email", validators=[DataRequired(),length(min=3,max=60)])
    password = PasswordField(label="Digite uma senha", validators=[DataRequired(), length(min=5,max=30), EqualTo("password_test")])
    password_test = PasswordField(label="Confirme a senha",validators=[DataRequired(),length(min=5,max=30)])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField(label="Digite seu username", validators=[DataRequired(),length(min=3,max=30)])
    password = PasswordField(label="Senha", validators=[DataRequired(), length(min=5,max=30)])
    submit = SubmitField()

class UserPostForm(FlaskForm):
    title = StringField(label="Título da Postagem",validators=[DataRequired(),length(min=2,max=30)])
    author = StringField(label="Autor",validators=[DataRequired(),length(min=2,max=30)])
    slug =  StringField(label="Assunto",validators=[DataRequired(),length(min=2,max=30)])
    content = TextAreaField(label="Conteúdo", validators=[DataRequired(), length(min=1)])
    submit = SubmitField()