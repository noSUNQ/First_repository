# project/app/main/routes.py

from flask import render_template, redirect, url_for, session
from app.models import User
from . import bp

@bp.route("/")
def index():
    if not session.get("logged"):
        return redirect(url_for("auth.index"))
    
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        is_admin = user and user.role == "admin"
    
    return render_template("main/index.html", is_admin=is_admin)

