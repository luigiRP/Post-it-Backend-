from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType, force_auto_coercion
import enum


db = SQLAlchemy()
force_auto_coercion()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), unique=False, nullable=False)
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
            "name": self.name,
        }
    
    @classmethod
    def post_user(cls, data_user):
        new_user = cls(username=data_user["username"], password=data_user["password"], email=data_user["email"], name=data_user["name"])
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def get_user(new_id):
        user = User.query.filter_by(id = new_id).first()        
        if user is None:
            return None
        else:       
            return user.serialize()

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False, unique=False)
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
    
    @classmethod
    def post_social(cls, data_social):
        new_social = cls(social_name=data_social["social_name"], username=data_social["username"], email=data_social["email"], password=data_social["password"], photo=data_social["photo"])
        db.session.add(new_social)
        db.session.commit()
        return new_social

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

    @classmethod
    def post_posts(cls, posting):
        new_post = cls(date = posting["date"], description = posting["description"])
        db.session.add(new_post)
        db.session.commit()
        return new_post

   
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
    
    @classmethod
    def post_multimedia(cls, data_multimedia):
        new_multimedia = cls(multimedia_type=data_multimedia["multimedia_type"], multimedia_url=data_multimedia["multimedia_url"])
        db.session.add(new_multimedia)
        db.session.commit()
        return new_multimedia