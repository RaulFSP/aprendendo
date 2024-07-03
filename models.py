from app import db
from sqlalchemy import Text, String, Integer, DateTime, ForeignKey, Boolean
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
    status = mapped_column(Boolean, unique=False,default=True)
    profile_pic = mapped_column(String(256), nullable=False)
    posts = relationship('UserPostModel', backref='poster')

class UserPostModel(db.Model):
    __tablename__ = "userpostmodel"
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    title = mapped_column(String(30),nullable=False)
    user_id = mapped_column(Integer, ForeignKey('usermodel.id'))
    # author = mapped_column(String(30),nullable=False)
    slug = mapped_column(String(30),nullable=False)
    content = mapped_column(Text,nullable=False)
    date_posted = mapped_column(DateTime,default=datetime.utcnow())