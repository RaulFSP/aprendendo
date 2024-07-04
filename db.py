from app import app,db
from models import *
import pymysql

def create_database(db_name, host="localhost", user="root", passwd="12345678"):
    try:
        connection = pymysql.connect(host=host, user=user, passwd=passwd)
        cursor = connection.cursor()
        sql = f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        cursor.execute(sql)
        connection.close()
    except pymysql.Error as e:
        return str(e)

with app.app_context():
    create_database("atividade_votacao")
    db.drop_all()
    db.create_all()