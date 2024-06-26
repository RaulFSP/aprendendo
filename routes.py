from app import app,db
from flask import render_template, redirect, url_for, flash
from models import UserModel
from forms import UserForm
from werkzeug.security import generate_password_hash, check_password_hash

@property
def password(self):
    raise AttributeError("Password not readable")

@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)

def verify_password(self,password):
    return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user',methods=['POST','GET'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = UserModel(
            name = form.name.data,
            email = form.email.data,
            password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        )
        form = UserForm(formdata=None)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuário {user.name} adicionado!')
        return redirect(url_for('add_user'))
    else:
        users = UserModel.query.order_by(UserModel.id).all()
        return render_template('user.html',form=form,users=users)

@app.route('/alter_user/<int:id>', methods=['POST','GET'])
def alter_user(id):
    form = UserForm()
    user = UserModel.query.get_or_404(id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        form = UserForm(formdata=None)
        db.session.commit()
        flash(f'Usuário {user.name} alterado!')
        return redirect(url_for('add_user'))
    else:
        return render_template('alter_user.html',form=form, user=user)