from app import db
from sqlalchemy import Text, String, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import mapped_column, relationship
from flask_login import UserMixin
from datetime import datetime

class UserModel(db.Model, UserMixin):
    __tablename__ = "usermodel"
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    name = mapped_column(String(100), nullable=False)
    username = mapped_column(String(30), nullable=False,unique=True)
    email = mapped_column(String(60), nullable=False, unique=True)
    password_hash = mapped_column(String(128), nullable=False)
    profile_pic = mapped_column(String(256), nullable=True)
    status = mapped_column(Boolean, unique=False,default=True)
    score = mapped_column(Float, default=0.0, nullable=False)
    cozinheiro = mapped_column(Boolean, unique=False)
    data_entrada = mapped_column(DateTime,default=datetime.now())
    posts = relationship('UserPostModel', backref='poster')
    user_endereco = relationship('UserEnderecoModel', backref='user_endereco')
    compra_model = relationship('CompraModel', backref='usuario')


class UserEnderecoModel(db.Model):
    __tablename__ = "user_endereco"
    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('usermodel.id'))
    cep = mapped_column(Text, nullable=False)
    numero = mapped_column(Text, nullable=False)
    bairro  = mapped_column(Text, nullable=False)
    endereco = mapped_column(Text, nullable=False)
    complemento = mapped_column(Text, nullable=True)

class UserPostModel(db.Model):
    __tablename__ = "userpostmodel"
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('usermodel.id'))
    name = mapped_column(String(30),nullable=False)
    categoria = mapped_column(String(30),nullable=False)
    content = mapped_column(Text,nullable=False)
    preco = mapped_column(Float,nullable=False)
    prato_pic = mapped_column(String(256), nullable=True)
    status = mapped_column(Boolean, unique=False, default=True)
    carrinho = relationship('CarrinhoModel', backref='carrinho')
    compra_model = relationship('CompraModel', backref='postagem')
    
class CarrinhoModel(db.Model):
    __tablename__ = "carrinhomodel"
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    id_cliente = mapped_column(Integer, ForeignKey('usermodel.id'))
    id_prato = mapped_column(Integer, ForeignKey('userpostmodel.id'))
    id_cozinheiro = mapped_column(Integer,nullable=False)
    name_cliente = mapped_column(Text, nullable=True)
    prato_preco = mapped_column(Float,nullable=False)
    qtd = mapped_column(Integer,nullable=True)
    total = mapped_column(Float, default=0.0, nullable=True)
    
    
class CompraModel(db.Model):
    __tablename__ = "compra_model"
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    id_cliente = mapped_column(Integer, ForeignKey('usermodel.id'))
    id_prato = mapped_column(Integer, ForeignKey('userpostmodel.id'))
    name_cliente = mapped_column(Text, nullable=True)
    id_cozinheiro = mapped_column(Integer,nullable=False)
    prato_preco = mapped_column(Float,nullable=False)
    qtd = mapped_column(Integer,nullable=True)
    status = mapped_column(Boolean, unique=False, default=True)
    total = mapped_column(Float, default=0.0, nullable=True)
    date_posted = mapped_column(DateTime,default=datetime.now())
    situacao = mapped_column(Text,default="pendente")