# project/app/questions/__init__.py

from flask import Blueprint

bp = Blueprint("questions", __name__,
               template_folder="templates",
               static_folder="static",
               static_url_path="/questions-static"
               )
from . import routes
