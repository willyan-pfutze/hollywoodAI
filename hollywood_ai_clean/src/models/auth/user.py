from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from datetime import datetime

# Importação temporária para desenvolvimento
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)  # Pode ser nulo para autenticação social
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos para autenticação social
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    facebook_id = db.Column(db.String(100), unique=True, nullable=True)
    
    # Relacionamento com vídeos (será implementado posteriormente)
    # videos = db.relationship('Video', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
