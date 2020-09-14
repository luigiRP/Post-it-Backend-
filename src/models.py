from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(
    PasswordType(schemes=['pbkdf2_sha512']),
    unique=False,
    nullable=False,
    )
    email = db.Column(db.String(320), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    social = db.relationship('Social', backref='user', lazy=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"User {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username, 
            "email": self.email,
            "name": self.name
        }



class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']),
    unique=False,
    nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=False)
    social_name = db.Column(db.Enum("instagram","twitter","facebook","linkedin"), nullable=False, unique=False)
    photo = db.Column(db.Text, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = relationship('Post',backref="social", lazy=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Social {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "social_name": self.social_name,
            "username": self.username, 
            "email": self.email,
            "photo": self.photo,
            "post_id": self.post_id,
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False, unique=False)
    description = db.Column(db.Text, nullable=False, unique=False)
    multimedias = db.relationship('Multimedia', backref='post', lazy=True)
    id_social = db.Column(db.Integer, db.ForeignKey('social.id'))
    is_active = db.Column(db.Boolean, default=True)
        
    def __repr__(self):
        return f"Post {self.description}"

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "id_multimedia": self.id_multimedia,
            "description": self.description
        }


    
class Multimedia(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    multimedia_type = db.Column(db.Enum("img","video"), nullable=False)
    multimedia_url = db.Column(db.Text,nullable=False, unique=False)
    is_active = db.Column(db.Boolean, default=True)
   
    id_post= db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Multimedia {self.multimedia_type}"

    def serialize(self):
        return {
            "id": self.id,
            "multimedia_type": self.multimedia_type,
            "multimedia_url": self.multimedia_url      
        }