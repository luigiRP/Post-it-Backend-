from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username= db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    social= db.relationship('Social', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.username

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

    

class Social(db.Model):
    social_name=db.Column(db.String(20), nullable=False, unique=False)
    password= db.Column(db.String(80), nullable=False, unique=False)
    username = db.Column(db.String(80), nullable=False, unique=False)
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(80), nullable=False, unique=False)
    photo= db.Column(db.String(80), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = relationship('Post',backref="social", lazy=True)

    def __repr__(self):
        return '<Social %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "social_name": self.social_name,
            "username": self.username, 
            "email": self.email,
            "photo": self.photo
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
    date=db.Column(db.Date, nullable=False, unique=False)
    id= db.Column(db.Integer, primary_key=True, nullable=False)
    description= db.Column(db.String(120), nullable=False, unique=False)
    multimedias= db.relationship('Multimedia', backref='post', lazy=True)
    id_social=db.Column(db.Integer, db.ForeignKey('social.id'))
    
    
    def __repr__(self):
        return '<Post %r>' % self.description

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "id_multimedia": self.id_multimedia,
            "description": self.description
        }
    
    def get_post(new_id_user,new_id_social,new_id_post):
        social = Social.query.filter_by(user_id=new_user_id,id=new_id_social).first()
        social=social.serialize()

    
class Multimedia(db.Model):
    id=db.Column(db.Integer,nullable=False, primary_key=True)
    multimedia_url= db.Column(db.String(250),nullable=False, unique=False)
   
    id_post= db.Column(db.Integer, db.ForeignKey('post.id'))
    def __repr__(self):
        return '<Multimedia %r>' % self.multimedia

    def serialize(self):
        return {
            "id": self.id,
            "multimedia_url": self.multimedia_url

        }






    