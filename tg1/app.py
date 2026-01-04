from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from urllib.parse import parse_qsl
import os
#import hmac
#import hashlib




# env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
KEY = os.getenv('KEY')

app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Убрать ошибку
db = SQLAlchemy(app)

# Session
app.secret_key = KEY

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

if __name__ == "__main__":
    app.run(port=5000, debug=True)