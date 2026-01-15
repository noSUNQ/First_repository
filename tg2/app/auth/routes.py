# project/app/auth/routes.py

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_mail import Message#, Mail
from app.models import User
from app.extensions import db, mail

bp = Blueprint("auth", __name__)

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

        session["otp"] = str(otp)
        session["email"] = email

        msg = Message(
            subject = "Код входа в СМИТ-СПОРТ",
            sender=1,
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
        return jsonify({"status": "error", "msg": "Неверный код", "color": "red"})
    
    session.pop("otp", None)
    session.pop("email", None)
    session["Logged"] = True

    return jsonify({"status": "success", "msg": "Успех", "color": "green"})