# SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
    "mysql+pymysql",
    "root",
    "12345678",
    "localhost",
    "3306",
    "integrador"
)
SECRET_KEY = "1235ceSD"
UPLOAD_FOLDER = 'static/temp/'