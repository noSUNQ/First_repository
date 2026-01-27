# project/app/admin/routes.py

from flask import render_template, request, redirect, url_for, jsonify
from app.extensions import db
from app.models import User
from . import bp

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("admin/index.html")

@bp.route("/users", methods=["GET", "POST"])
def users():

    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_username = request.form.get("username")
        new_role = request.form.get("role")

        user = User.query.get(user_id)
        if user:
            if new_username:
                user.username = new_username
            if new_role:
                user.role = new_role
            db.session.commit()
            return jsonify({"status": "success",
                            "message": "Обновленно!",
                            "username": user.username,
                            "role": user.role})
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 400
    
    users_list = User.query.all()
    return render_template("admin/users.html", users=users_list)