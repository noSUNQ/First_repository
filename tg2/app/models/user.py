# project/app/models/user.py

from app.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(50), default="user")

    #avatar_url = db.Column(db.String(200))
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chats = db.relationship("Chat", back_populates='author')
    messages = db.relationship("Message", back_populates='user')

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"