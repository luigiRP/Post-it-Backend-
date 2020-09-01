from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    social = db.relationship('Social', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username, 
            "email": self.email,
            "name": self.name
        }
    
    def get_user(new_id):
        user= User.query.filter_by(id=new_id).first()
        user = user.serialize()
        
        return user

    
 

class SocialEnum(enum.Enum):
    instagram = 'Instagram'
    facebook = 'Facebook'
    twitter = 'Twitter'
    linkedin = 'LinkedIn'

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=False)
    password = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(320), nullable=False, unique=False)
    social_name = db.Column(db.Enum("instagram","facebook","twitter","google"), nullable=False, unique=False)
    photo = db.Column(db.Text, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
        }
    
    def get_all_socials(new_id):
        socials = Social.query.filter_by(user_id=new_id)
        all_socials = list(map(lambda x: x.serialize(), socials))
        return all_socials
    
    def get_social(new_user_id, new_id_social):
        social = Social.query.filter_by(user_id=new_user_id,id=new_id_social).first()
        social=social.serialize()
        
        return social

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False, unique=False)
    description = db.Column(db.Text, nullable=False, unique=False)
    multimedias = db.relationship('Multimedia', backref='post', lazy=True)
    id_social = db.Column(db.Integer, db.ForeignKey('social.id'))
        
    def __repr__(self):
        return f"Post {self.description}"

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "id_social": self.id_social
        }
    
    def get_post(new_id_user,new_id_social,new_id_post):
        post = db.session.query().filter(User.id == Social.id).filter(Social.id == Post.id).filter(User.id==new_id_user, Social.id==new_id_social, Post.id==new_id_post).first()

class MultimediaEnum(enum.Enum):
    img = 'Img'
    video = 'Video'
    
class Multimedia(db.Model):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    multimedia_type = db.Column(db.Enum(MultimediaEnum), nullable=False)
    multimedia_url = db.Column(db.Text,nullable=False, unique=False)
    id_post= db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Multimedia {self.multimedia_type}"

    def serialize(self):
        return {
            "id": self.id,
            "multimedia_type": self.multimedia_type,
            "multimedia_url": self.multimedia_url      
        }





    