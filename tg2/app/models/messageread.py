# project/app/models/messageread.py

from app.extensions import db
from datetime import datetime

class MessageRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    
    __table_args__ = (db.UniqueConstraint("message_id", "user_id"),) # Уникальность

    def __repr__(self):
        return f'<MessageRead {self.id}: msg={self.message_id}, user={self.user_id}>'