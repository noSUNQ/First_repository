# project/app/questions/routes.py

from flask import render_template, request, session, jsonify, redirect
from app.extensions import db
from app.models import User, Chat, Message
from . import bp

@bp.route("/", methods=["GET", "POST"])
def index():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user.role == "employee":
        chats = Chat.query.filter_by(user_id=user_id).all()
        return render_template("questions/index.html", chats=chats)
    elif user.role == "engineer" or user.role == "admin":
        chats = Chat.query.all()
        return render_template("questions/index.html", chats=chats)
    else:
        return render_template("error.html", msg="Нет доступа")

@bp.post("/add_chat")
def add_chat():
    chat_name = request.form.get("chatName")
    user_id = session.get("user_id")

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"status": "error", "msg": "Пользователь не найден"})

    if user.role == "employee" or user.role == "engineer" or user.role == "admin":
        try:
            chat = Chat(user_id=user_id, name=chat_name)
            db.session.add(chat)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "msg": "Ошибка создания чата"})

        return jsonify({"status": "success"})
    return jsonify({"status": "error", "msg": "Нет доступа"})

@bp.get("/chat/<int:chat_id>")
def chat(chat_id):
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if not user:
        #return jsonify({"status": "error", "msg": "Пользователь не найден"})
        return render_template("error.html", msg="Пользователь не найден") 
    if user.role not in ["admin", "engineer", "employee"]:
        #return jsonify({"status": "error", "msg": "Нет доступа"})
        return render_template("error.html", msg="Нет доступа") 

    chat = Chat.query.filter_by(id=chat_id).first()
    messages = Message.query.filter_by(chat_id=chat_id).all()

    return render_template("chat.html", chat=chat, messages=messages)

@bp.post("/send_message")
def send_message():
    data = request.form.get("")
    text = data.get("text", "").strip()
    media = data.get("media")
    chat_id = data.get("chat_id")
    user_id = session.get("user_id")

    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat_id in chat:
        return jsonify({"status": "error", "msg": "Чат не найден"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if not user or user.role not in ["admin", "engineer", "employee"]:
        return jsonify({"status": "error", "msg": "Нет доступа"}), 403
    
    if text:
        try:
            msg_type = "text"
            msg = Message(type="text", text=text, chat_id=chat_id, user_id=user_id)
            db.session.add(msg)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "msg": str(e)}), 400
        

    if media:
        for file in media:
            # Определяем тип? type
            # Сохраняем медиа на диск
            # Формируем ссылку или путь link
            try:
                msg = Message(type=type, text=link, chat_id=chat_id, user_id=user_id)
                db.session.add(msg)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"status": "error", "msg": str(e)}), 400

    return jsonify({"status": "success"})