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

    def get_user(new_id):
        user= User.query.filter_by(id=new_id,is_active=True).first()        
        if not user:
            return None
        else:       
            return user.serialize()
    
    def delete_user(new_id):
        user = User.query.filter_by(id=new_id, is_active=True).first() 
        if user is None:
            return None
        else:
            user.is_active = False
            db.session.commit()
            return "User deleted"
    
    def update_user(new_id,body):
        user= User.query.filter_by(id=new_id, is_active=True).first() 
        if user is None:
            return None
        else:
            if "username" in body:
                user.username = body["username"]
            if "email" in body:
                user.email = body["email"]
            if "name" in body:
                user.name = body["name"]
            if "password" in body:
                user.password = body["password"]
            db.session.commit()
            return "user with id: " + str(user.id) + " updated"
        
    def get_user_by_email(new_email, new_password):
        user = User.query.filter_by(email = new_email, password=new_password, is_active=True).first()
        if not user:
            return None
        if "username" in body:
            user.username = body["username"]
        if "email" in body:
            user.email = body["email"]
        if "name" in body:
            user.name = body["name"]
        if "password" in body:
            user.password = body["password"]
        db.session.commit()
        return user

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
    
    def update_social(new_user_id, new_id_social):
        user = User.get_user(new_user_id)
        if user is None:
            return User.get_user(new_user_id)
        else:
          social = Social.query.filter_by(user_id=new_user_id,id=new_id_social, is_active=True).first()
          if social is None:
              return None
          else:
              if "social_name" in body:
                  social.social_name = body["social_name"]
              if "email" in body:
                  social.email = body["email"]
              if "username" in body:
                  social.username = body["username"]
              if "password" in body:
                  social.password = body["password"]
              db.session.commit()
              return social
            
    def delete_social(new_user_id,new_id_social):
        user = User.get_user(new_user_id)
        social = Social.query.filter_by(user_id=new_user_id,id=new_id_social, is_active=True).first()
        if user is None or social is None:
            return None
        else:
            social.is_active = False
            db.session.commit()
            return "Social media account deleted"

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

    

    def update_post(new_id_user,new_id_social,new_id_post,body):
        social= Social.get_social(new_id_user,new_id_social)
        post = Post.query.filter_by(id_social=new_id_social,id=new_id_post, is_active=True).first()
        if not post or not social:
            return None
        else:
            posts = Post.query.filter_by(id_social=new_id_social, is_active=True)
            posts = list(map(lambda x: x.serialize(), posts))
            if len(posts) is 0:
                return None
            else:
                return posts
            
    
    def delete_post(new_user_id,new_id_social,new_id_post):
        user = User.get_user(new_user_id)
        social = Social.get_social(new_user_id,new_id_social)
        post = Post.query.filter_by(id_social=new_id_social,id=new_id_post, is_active=True).first()
        
        if user is None or social is None or post is None:
            return None
        else:
            post.is_active = False
            db.session.commit()
            return "Post deleted"

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
          
    def get_all_multimedia(new_id_user,new_id_social,new_id_post):
        post = Post.get_post(new_id_user,new_id_social,new_id_post)
        social = Social.get_social(new_id_user,new_id_social)
        user = User.get_user(new_id_user)
        if not user or not social or not post:
            return None
        else:
            multimedias = Multimedia.query.filter_by(id_post=new_id_post,is_active=True)
            multimedias = list(map(lambda x: x.serialize(), multimedias))
            if len(multimedias) is 0:
                return None
            else:
                return multimedias
    
    def get_multimedia(new_id_user,new_id_social,new_id_post,new_id_multimedia):
        post = Post.get_post(new_id_user,new_id_social,new_id_post)
        social = Social.get_social(new_id_user,new_id_social)
        user = User.get_user(new_id_user)
        if not user or not social or not post:
            return None
        else:
            multimedia = Multimedia.query.filter_by(id_post=new_id_post, id=new_id_multimedia,is_active=True).first()
            if not multimedia:
                return None
            else:
                return multimedia.serialize()
    
    def delete_multimedia(new_user_id,new_id_social,new_id_post,new_id_multimedia):
        user = User.get_user(new_user_id)
        social = Social.get_social(new_user_id,new_id_social)
        post = Post.get_post(new_user_id,new_id_social,new_id_post)
        multimedia = Multimedia.query.filter_by(id_post=new_id_post, id=new_id_multimedia, is_active=True).first()
        
        if user is None or social is None or post is None or multimedia is None:
            return None
        else:
            multimedia.is_active = False
            db.session.commit()
            return "Multimedia deleted"
