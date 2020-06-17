import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3' #os.environ.get("DATABASE_URL")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")