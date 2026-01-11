from flask import Flask, render_template, request, session, render_template_string, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = 'sadasdasdasfas'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 587 #465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False #True for 465
mail = Mail(app)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    email = data.get('email')

    otp = "123456"

    session["otp"] = str(otp)
    session["otp_email"] = email
    
    subject = "Код входа в ЭЖВ"
    message = f"Ваш 6-значный код для входа: {otp}"

    msg = Message(
        subject, 
        sender=os.getenv('EMAIL'), 
        recipients=[email]
        )

    msg.body = message
    mail.send(msg)

    return jsonify({"status": "success"}), 200

@app.post("/verify")
def verify():
    data = request.json
    otp = str(data.get("otp"))
    otp_email = data.get("otp_email")

    if session.get("otp") != otp or session.get("otp_email") != otp_email:
        return jsonify({"status": "error"}), 400
    
    session.pop('otp', None)
    session.pop('otp_email', None)
    session["Login"] = True

    
    
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)