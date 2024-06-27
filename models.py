from app import db
from sqlalchemy import Text, String, Integer, DateTime
from sqlalchemy.orm import mapped_column
from datetime import datetime
class UserModel(db.Model):
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    name = mapped_column(String(100), nullable=False)
    email = mapped_column(String(60), nullable=False, unique=True)
    password_hash = mapped_column(String(128), nullable=False)

class UserPostModel(db.Model):
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    title = mapped_column(String(30),nullable=False)
    author = mapped_column(String(30),nullable=False)
    slug = mapped_column(String(30),nullable=False)
    content = mapped_column(Text,nullable=False)
    date_posted = mapped_column(DateTime,default=datetime.utcnow())