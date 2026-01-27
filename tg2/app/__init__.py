# project/app/__init__.py

from flask import Flask
from .extensions import db, migrate, mail
from config import Config
#import os

def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder="../static", 
                static_url_path="/static", 
                template_folder="../templates")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .questions import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix="/questions")

    return app
