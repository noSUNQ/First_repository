# project/app/models/message.py

from app.extensions import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(1000))
    type = db.Column(db.String(20), default="text") # text / image / video / file
    reply_to_id = db.Column(db.Integer, db.ForeignKey("message.id"), nullable=True) # сообщение на которое отвечаем
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    edited_at = db.Column(db.DateTime, nullable=True) 
    #is_read = db.Column(db.Boolean, default=False) # статус прочтения


    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False, index=True)

    user = db.relationship("User", back_populates="messages")
    chat = db.relationship("Chat", back_populates="messages")

    def __repr__(self):
        return f'<Message id={self.id}, chat={self.chat_id}, user={self.user_id}, text="{self.text[:50]}...">'
    