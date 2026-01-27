# project/app/auth/routes.py

from flask import render_template, request, session, redirect, url_for, jsonify
from flask_mail import Message
from app.models import User
from app.extensions import db, mail
from . import bp
import os


@bp.route("/", methods=["GET", "POST"])
def index():
    if session.get("logged"):
        return redirect(url_for("main.index"))
    return render_template("auth/index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter
        # Доделать

@bp.post("/send_otp")
def send_otp():
    data = request.get_json()
    email = data.get("valueEmail")
    if email:   
        
        otp = "123456"  # Добавить генерацию otp 
        #otp = f"{random.randit(1000000,999999)}"

        session["otp"] = str(otp)
        session["email"] = email

        msg = Message(
            subject = "Код входа в СМИТ-СПОРТ",
            recipients=[email],
            body="Ваш 6-ти значный код для входа: " + otp
        )
        
        mail.send(msg)
        return jsonify({"status": "success", "msg": "Код отправлен на почту", "color": "green"}), 200

@bp.post("/verify")
def verify():
    data = request.get_json()
    otp = str(data.get("valueOtp"))
    email = data.get("valueEmail")

    if session.get("otp") != otp or session.get("email") != email:
        return jsonify({"status": "error", "msg": "Неверный код", "color": "red"}), 400
    
    session.pop("otp", None)
    session.pop("email", None)
    session["logged"] = True

    user = User.query.filter_by(email=email).first()
    if not user:
        try:
            username = email.split('@')[0][:64]
            user = User(email=email, username=username)
            if email == os.getenv("MAIL_USERNAME"):
                user.role = "admin"
            else:
                user.role = "user"
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "msg": "Ошибка создания ползователя", "color": "red"}), 500
    else: 
        session["user_id"] = user.id

    session["user_id"] = user.id
    return jsonify({"status": "success", "msg": "Успех", "color": "green"}), 200

@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))