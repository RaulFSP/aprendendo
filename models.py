from app import db
from sqlalchemy import Text, String, Integer
from sqlalchemy.orm import mapped_column

class UserModel(db.Model):
    id = mapped_column(Integer,autoincrement=True,primary_key=True)
    name = mapped_column(String(100), nullable=False)
    email = mapped_column(String(60), nullable=False)
    password_hash = mapped_column(String(128), nullable=False)
