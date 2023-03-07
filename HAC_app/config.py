import os

class Config:
    SECRET_KEY = token = os.environ.get("key")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
