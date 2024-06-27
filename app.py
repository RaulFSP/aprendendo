from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile("config.py")
csrf = CSRFProtect(app)
csrf.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)
login_manager = LoginManager()
login_manager.init_app(app)




from routes import *

if __name__ == "__main__":
    app.run(debug=True)
    