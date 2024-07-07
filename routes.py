from app import app,db, login_manager
from flask import render_template, redirect, url_for, flash
from models import UserModel, UserPostModel, UserEnderecoModel
from forms import UserForm, LoginForm, UserPostForm, SearchForm, AlterUserForm, AlterUserPasswordForm
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from uuid import uuid1
import os


# flask login
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get_or_404(user_id)

# password hash
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
    pratos = UserPostModel.query.filter(UserPostModel.status == True).all()
    cozinheiros = UserModel.query.filter(UserModel.status == True).all()
    return render_template('index.html',pratos=pratos, cozinheiros=cozinheiros)

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        foto = form.profile_pic.data
        profile_pic = None
        if foto:
            profile_pic = "{}_{}".format(uuid1(), secure_filename(foto.filename))
            try:
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
            except Exception as e:
                flash('Error uploading the picture')
                return redirect(url_for('add_user'))

        user = UserModel(
            name=form.name.data,
            email=form.email.data,
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data, method='pbkdf2:sha256'),
            profile_pic=profile_pic,
            cozinheiro=form.cozinheiro.data == 'True'
        )
        db.session.add(user)
        db.session.commit()
        endereco = UserEnderecoModel(
            user_id=user.id,
            cep=form.cep.data,
            numero=form.numero.data,
            bairro=form.bairro.data,
            endereco=form.endereco.data,
            complemento=form.complemento.data
        )
        db.session.add(endereco)
        db.session.commit()
        form = UserForm(formdata=None)
        flash(f'User {user.name} added!')
        return redirect(url_for('add_user'))

    return render_template('user.html', form=form)



@app.route('/alter_user/<int:id>', methods=['POST','GET'])
@login_required
def alter_user(id):
    form = AlterUserForm(cozinheiro=current_user.cozinheiro)
    user = UserModel.query.get_or_404(id)
    endereco = UserEnderecoModel.query.filter(UserEnderecoModel.user_id==current_user.id).first_or_404()
    if form.validate_on_submit():
        foto = form.profile_pic.data
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
        user.cozinheiro = form.cozinheiro.data == 'True'
        endereco.cep = form.cep.data
        endereco.numero = form.numero.data
        endereco.bairro = form.numero.data
        endereco.endereco = form.endereco.data
        endereco.complemento = form.complemento.data
        if foto != None:
            if user.profile_pic != None:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.profile_pic))
            profile_pic = "{}_{}".format(uuid1(),secure_filename(foto.filename))
            user.profile_pic = profile_pic
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
        form = AlterUserForm(formdata=None)
        db.session.commit()
        flash(f'Informações do usuário \'{current_user.username}\' alterada!')
        return redirect(url_for('dashboard_user'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')
    return render_template('alter_user.html',form=form, user=user, endereco=endereco)

@app.route('/desabilitar_usuario')
@login_required
def desativar_usuario():
    user = UserModel.query.get_or_404(current_user.id)
    user.status = False
    db.session.commit()
    flash(f'{current_user.username} foi desabilitado')
    return redirect(url_for('dashboard_user'))

@app.route('/habilitar_usuario')
@login_required
def ativar_usuario():
    user = UserModel.query.get_or_404(current_user.id)
    user.status = True
    db.session.commit()
    flash(f'{current_user.username} foi habilitado')
    return redirect(url_for('dashboard_user'))

@app.route('/alter_user_password/<int:id>', methods=['POST','GET'])
@login_required
def alter_user_password(id):
    form = AlterUserPasswordForm()
    user = UserModel.query.get_or_404(id)
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user.password_hash = password_hash
        form = AlterUserPasswordForm(formdata=None)
        db.session.commit()
        flash(f'Senha do usuário \'{current_user.username}\' alterada!')
        return redirect(url_for('dashboard_user'))
    else:
        return render_template('alter_user_password.html',form=form, user=user)


@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    form = UserPostForm()
    if form.validate_on_submit():
        user_id = current_user.id
        foto = form.prato_pic.data
        prato_pic = None
        if foto:
            prato_pic = "{}_{}".format(uuid1(), secure_filename(foto.filename))
            try:
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], prato_pic))
            except Exception as e:
                flash('Deu erro')
                return redirect(url_for('add_post'))
        
        post = UserPostModel(
            user_id=user_id,
            name=form.name.data,
            categoria=form.categoria.data,
            content=form.content.data,
            preco=form.preco.data,
            prato_pic=prato_pic
        )
        form = UserPostForm(formdata=None)
        db.session.add(post)
        db.session.commit()
        flash(f'{post.name} adicionado!')
        
        return redirect(url_for('add_post'))
    else:
        return render_template('user_post.html', form=form)

@app.route('/alterar/<int:id>',methods=['POST','GET'])
@login_required
def alter_post(id):
    form = UserPostForm()
    post = UserPostModel.query.get_or_404(id)
    if post.poster.id == current_user.id:
        if form.validate_on_submit():
            foto = form.prato_pic.data
            if foto:
                if post.prato_pic != None:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.prato_pic))
                prato_pic = "{}_{}".format(uuid1(),secure_filename(foto.filename))
                post.prato_pic = prato_pic
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], prato_pic))
            post.name = form.name.data
            post.categoria=form.categoria.data
            post.content = form.content.data
            post.preco = form.preco.data
            form = UserPostForm(formdata=None)
            db.session.commit()
            flash(f'{post.name} Alterado!')
            return redirect(url_for('dashboard_user'))
        else:
            form.name.data = post.name
            form.categoria.data = post.categoria 
            form.content.data = post.content
            
            form.prato_pic.data = post.prato_pic
            form.preco.data = post.preco
            return render_template('alter_post.html',form=form, post=post)
    else:
        flash('Você não pode alterar esse prato!')
        return redirect(url_for('index'))

@app.route('/desabilitar/<int:id>')
@login_required
def desabilitar_prato(id):
    post = UserPostModel.query.get_or_404(id) 
    if current_user.id == post.poster.id:
        post.status = False
        db.session.commit()
        flash(f"{post.name} desabilitado!")
        return redirect(url_for('dashboard_user'))
    else:
        flash(f"Você não pode deletar esse prato!")
        return redirect(url_for('index'))

@app.route('/ativar/<int:id>')
@login_required
def habilitar_prato(id):
    post = UserPostModel.query.get_or_404(id) 
    if current_user.id == post.poster.id:
        post.status = True
        db.session.commit()
        flash(f"{post.name} habilitado!")
        return redirect(url_for('dashboard_user'))
    else:
        flash(f"Você não pode deletar esse prato!")
        return redirect(url_for('index'))


@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            password = form.password.data
            if check_password_hash(user.password_hash, password):
                login_user(user)
                flash(f"{user.username} logado!")
                form = LoginForm(formdata=None)
                return redirect(url_for('index'))
            else:
                flash("Senha incorreta!")
                return redirect(url_for('login'))
        else:
            flash("Usuário não encontrado!")
            return redirect(url_for('login'))
    else:
        return render_template('login.html',form=form)

@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    flash(f"Usuário {current_user.username} deslogado")
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['POST','GET'])
@login_required
def dashboard_user():
    user = UserModel.query.get_or_404(current_user.id)
    pratos = UserPostModel.query.filter(UserPostModel.user_id==current_user.id).all()
    endereco = UserEnderecoModel.query.filter(UserEnderecoModel.user_id==current_user.id).first_or_404()
    return render_template('dashboard.html',user=user, pratos=pratos, endereco=endereco)


@app.route('/cozinheiros', methods=['POST','GET'])
def listar_usuarios():
    form = SearchForm()
    cozinheiros = UserModel.query.filter(UserModel.status == True, UserModel.cozinheiro == True).all()
    if form.validate_on_submit():
        search = form.search.data
        cozinheiros = UserModel.query.filter(UserModel.username.like('%{}%'.format(search)), UserModel.cozinheiro == True).all()
        form = SearchForm(formdata=None)    
    return render_template('cozinheiros.html',cozinheiros=cozinheiros, form=form)

@app.route('/menu/<username>',methods=['POST','GET'])
def menu_cozinheiro(username):
    cozinheiro = UserModel.query.filter(UserModel.username == username).first_or_404()
    pratos = UserPostModel.query.filter(UserPostModel.user_id == cozinheiro.id).all()
    endereco = UserEnderecoModel.query.filter(UserEnderecoModel.user_id==cozinheiro.id).first_or_404()
    return render_template('menu_cozinheiro.html',cozinheiro=cozinheiro, pratos=pratos, endereco=endereco)