from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from urllib.parse import parse_qsl
import os
#import hmac
#import hashlib
from admin.admin import admin

from flask_mail import Mail, Message

import secrets
import time


# env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
KEY = os.getenv('KEY')

app = Flask(__name__)

# Blueprint
app.register_blueprint(admin, url_prefix='/admin')

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Убрать ошибку
db = SQLAlchemy(app)

# Session
app.secret_key = KEY

# Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 587 #465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False #True for 465
mail = Mail(app)

# Integer String(size) Text DateTime Float Boolean LargeBinary 
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    profiles = db.relationship('Profiles', backref='user', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"

class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")

@app.route("/people")
def people():
    return render_template("/people")
        
@app.route("/create_tables", methods={"POST"})
def create_tables():
    with app.app_context():
        db.create_all()
    return jsonify({"status": "tables created"})

@app.route("/drop_tables")
def drop_tables():
    with app.app_context():
        db.drop_all()
        
@app.route("/add_person", methods=["POST"])
def add_person():
    #if request.method == "POST":
    try:
        hash = generate_password_hash(request.form['psw'])
        u = Users(email=request.form['email'], psw=hash)
        db.session.add(u)
        db.session.flush()

        p = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id = u.id)
        db.session.add(p)
        db.session.commit()
        return jsonify({"status": "success"})
    except:            
        db.session.rollback()
        print("Ошибка добавления в БД")
        return jsonify({"status": "error"}), 400

'''    
@app.route("/send_cod", methods=["POST"])
def send_cod():
    try:
        name = "Vadim"
        email = os.getenv('EMAIL2')
        subject = "Subject"
        message = "this is message"
        msg = Message(subject, sender = os.getenv('EMAIL'), recipients = [email])
        msg.body = ('Hello ' + name + ",\n\n" + message)
        mail.send(msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Mail error: {e}") # Для логов
        return jsonify({"error": str(e)}), 500
'''
    
@app.post("/send_code")
def send_code():
    try:
        data = request.json
        user_email = data.get('email')
        if not user_email:
            return jsonify({"error": "Email required"}), 400
        
        otp = f"{secrets.randbelow(1000000):06d}"

        session['otp'] = otp
        session['otp_email'] = user_email
        session['otp_time'] = time.time()

        subject = "Код входа в ЭЖВ"
        message = f"Ваш 6-значный код для входа: {otp}\n\nКод действителен 5 минут"

        msg = Message(subject, sender=os.getenv('EMAIL'), recipients=[user_email])
        msg.body = message
        mail.send(msg)

        return jsonify({"status": "success", "message": "Код отправлен"}), 200
    except Exception as e:
        print(f"Mail error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.post("/verify_code")
def verify_code():
    try:
        data = request.json
        user_email = data.get('email')
        user_otp = data.get('otp')

        if session.get('otp_email') != user_email or session.get('otp') != user_otp:
            return jsonify({"error": "Неверный код"}), 400
        
        if time.time() - session.get('otp_time', 0) > 300:
            return jsonify({"error": "Код истек"}), 400
        
        session.pop('otp', None)
        session.pop('otp_email', None)
        session.pop('otp_time', None)
        session['logged_in'] = True

        return jsonify({"status": "success", "message": "Вход успешен"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)