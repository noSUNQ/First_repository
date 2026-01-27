# project/app/models/chat.py

from app.extensions import db
from datetime import datetime

'''
chat_members = db.Table(
    "chat_members",
    db.Column("chat_id", db.Integer, db.ForeignKey("chat.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("joined_at", db.DateTime, default=datetime.utcnow),
)
'''

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True) # name вместо title
    #avater_url - URL аватара чата
    #text = db.Column(db.Text, nullable=False) #Убрать, а вместо будет первое сообщение
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #status = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    messages = db.relationship('Message', back_populates='chat', lazy='dynamic')
    author = db.relationship('User', back_populates='chats')
    
    def __repr__(self):
        return f'<Chat {self.id}: "{self.name[:50]}..." [author={self.user_id}]>'