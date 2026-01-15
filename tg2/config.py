# project/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587 # or 465
    MAIL_USE_TLS = True # or False
    MAIL_USE_SSL = False # or True
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD")
    MAIL_DAFEULT_SENDER = os.getenv("EMAIL")
