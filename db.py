from app import app,db
from models import UserModel
with app.app_context():
    db.drop_all()
    db.create_all()