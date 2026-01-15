from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone



app = Flask(__name__)
app.secret_key = 'askfhsdckjg'

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Убрать ошибку
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(50))

    chats = db.relationship('Chats', backref='user', lazy=True)
    messages = db.relationship('Messages', backref='user', lazy=True)
    notifications = db.relationship('Notifications', backref='user', lazy=True)
    media = db.relationship('Media', backref='user', lazy=True)


    def __repr__(self):
        return f"<users {self.id}>"

class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    name = db.Column(db.String(150))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    messages = db.relationship('Messages', backref='chat', lazy=True)
    notifications = db.relationship('Notifications', backref='chat', lazy=True)
    media = db.relationship('Media', backref='chat', lazy=True)

    def __repr__(self):
        return f"<chats {self.id}>"

class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))

    media = db.relationship('Media', backref='message', uselist=False)

    def __repr__(self):
        return f"<messages {self.id}>"
    
class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))

    def __repr__(self):
        return f"<notifications {self.id}>"
    
class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    link = db.Column(db.String(250))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))

    def __repr__(self):
        return f"<media {self.id}>"

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/chats")
def chats():
    chats = Chats.query.all()
    return render_template("chats.html", chats=chats)

@app.route("/chat/<int:chat_id>")
def chat_detail(chat_id):
    chat = Chats.query.get(chat_id)
    msgs = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).all() 
    return render_template("chat.html", chat=chat, msgs=msgs)
    
@app.route("/create_tables", methods={"POST"})
def create_tables():
    with app.app_context():
        db.create_all()
    return jsonify({"status": "tables created"})

@app.post("/drop_tables")
def drop_tables():
    with app.app_context():
        db.drop_all()
    return jsonify({"status": "tables deleted"})

@app.post("/add_user")
def add_user():
    data = request.json
    email = data.get("email")
    role = data.get("role")
    try:
        u = Users(email=email, role=role)
        db.session.add(u)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "error": str(e)}), 400
    
@app.post("/add_chat")
def add_chat():
    data = request.json
    name = data.get("name")
    status = data.get("status")
    user_email = data.get("email_session")
    try:
        user = Users.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"status": "Пользователь не найден"}), 404
        c = Chats(name=name, status=status, user_id=user.id)
        db.session.add(c)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "error": str(e)}), 400
    
@app.post("/add_message")
def add_message():
    data = request.json
    print("debug", data) #delete
    email_session = data.get("email_session")
    chats_id = data.get("chats_id")
    text = data.get("text")
    try:
        user = Users.query.filter_by(email=email_session).first()
        print("user found", user) #delete
        if not user:
            return jsonify({"status": "Пользователь не найден"}), 404
        c = Chats.query.get(chats_id)
        print("chat found", c) #delete
        if not c:
            return jsonify({"status": "Чат не найден"}), 404
        m = Messages(chat_id=c.id, text=text, user_id=user.id)
        db.session.add(m)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "error": str(e)}), 400
    
@app.post("/send_msg")
def send_msg():
    data = request.json()
    user_id = session.get("id")
    chat_id = data.get("chat_id")
    text = data.get("text")
    try:
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"status": "Пользователь не найден"}), 404
        c = Chats.query.get(chat_id)
        if not c:
            return jsonify({"status": "Чат не найден"}), 404
        m = Messages(chat_id=c.id, text=text, user = user_id)
        db.session.add(m)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "error": str(e)}), 400
    
@app.post("/add_msg")
def add_msg():
    chat_id = request.form.get("chat_id", type=int)
    text = request.form.get("text", "").strip()

    if not chat_id or not text:
        return jsonify({"error": "Пустое сообщение"}), 400
    
    chat = Chats.query.get(chat_id)
    if not chat:
        return jsonify({"error": "Чат не найден"}), 404
    
    msg = Messages(chat_id=chat_id, text=text)
    db.session.add(msg)
    db.session.commit()

    return jsonify({"id": msg.id, "text": msg.text})

if __name__ == "__main__":
    app.run(port=5000, debug=True)