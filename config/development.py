import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLALCHEMY_DATABASE_DRIVER = "postgresql+psycopg2"
SQLALCHEMY_DATABASE_HOSTNAME = "127.0.0.1"
SQLALCHEMY_DATABASE_USER = "root"
SQLALCHEMY_DATABASE_PASSWORD = "123"
SQLALCHEMY_DATABASE_NAME = "root"
SQLALCHEMY_DATABASE_URI = (
    f"{SQLALCHEMY_DATABASE_DRIVER}://"
    f"{SQLALCHEMY_DATABASE_USER}:{SQLALCHEMY_DATABASE_PASSWORD}"
    f"@{SQLALCHEMY_DATABASE_HOSTNAME}/{SQLALCHEMY_DATABASE_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_DOMAIN = "app.snoopy.com"
