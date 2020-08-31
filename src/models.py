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
            "name": self.name,
            "social_id": self.social_id,
        }
    
    def get_users():
        users = User.query.all()
        users = list(map(lambda user: user.serialize(),users))
        return users

    

class Social(db.Model):
    social_name=db.Column(db.String(20), nullable=False, unique=False)
    password= db.Column(db.String(80), nullable=False, unique=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(80), nullable=False, unique=True)
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
            "photo": self.photo,
            "post_id": self.post_id,
        }

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






    