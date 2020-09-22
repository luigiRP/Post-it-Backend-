from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    social = db.relationship('Social', backref='user', lazy=True)
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
    
    def delete_user(new_id):
        user = User.query.filter_by(id=new_id, is_active=True).first() 
        if not user:
            return None
        else:
            user.is_active = False
            db.session.commit()
            return "User deleted"

class SocialEnum(enum.Enum):
    instagram = 'Instagram'
    facebook = 'Facebook'
    twitter = 'Twitter'
    linkedin = 'LinkedIn'

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=False)
    social_name = db.Column(db.Enum("instagram","twitter","facebook","linkedin"), nullable=False, unique=False)
    photo = db.Column(db.Text, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    is_active = db.Column(db.Boolean, default=True)
    posts = relationship('Post',backref="social", lazy=True)
    
    def __repr__(self):
        return f"Social {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "social_name": self.social_name,
            "username": self.username,
            "email": self.email,
            "photo": self.photo,
            "user_id": self.user_id,
            "is_active": self.is_active
        }
    
    def delete_social(new_user_id,new_id_social):
        user = User.get_user(new_user_id)
        social = Social.query.filter_by(user_id=new_user_id,id=new_id_social, is_active=True).first()
        
        if not user or not social:
            return None
        else:
            social.is_active = False
            db.session.commit()
            return social

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
            "id_social": self.id_social
        }
    
    def delete_post(new_user_id,new_id_social,new_id_post):
        user = User.get_user(new_user_id)
        social = Social.get_social(new_user_id,new_id_social)
        post = Post.query.filter_by(id_social=new_id_social,id=new_id_post, is_active=True).first()
        
        if user is None or social is None or post is None:
            return None
        else:
            post.is_active = False
            db.session.commit()
            return post.serialize()

class Multimedia(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    multimedia_type = db.Column(db.Enum("img","video"), nullable=False)
    multimedia_url = db.Column(db.Text,nullable=False, unique=False)
    id_post= db.Column(db.Integer, db.ForeignKey('post.id'))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Multimedia {self.multimedia_type}"

    def serialize(self):
        return {
            "id": self.id,
            "multimedia_type": self.multimedia_type,
            "multimedia_url": self.multimedia_url
        }
    
    def delete_multimedia(new_user_id,new_id_social,new_id_post,new_id_multimedia):
        user = User.get_user(new_user_id)
        social = Social.get_social(new_user_id,new_id_social)
        post = Post.get_post(new_user_id,new_id_social,new_id_post)
        multimedia = Multimedia.query.filter_by(id_post=new_id_post, id=new_id_multimedia, is_active=True).first()
        
        if not user or not social or not post or not multimedia:
            return None
        else:
            multimedia.is_active = False
            db.session.commit()
            return multimedia.serialize()

