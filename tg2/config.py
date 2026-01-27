# project/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Почта
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587 # or 465
    MAIL_USE_TLS = True # or False
    MAIL_USE_SSL = False # or True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
