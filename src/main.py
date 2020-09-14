"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Social, Post, Multimedia



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_user(id)
    if not user:
        raise APIException('User not found', status_code=404)
    return user

@app.route('/login', methods=['GET'])
def get_user_by_email():
    body=request.get_json()

    user = User.get_user_by_email(body["email"],body["password"])
    if not user:
        raise APIException("Login failed", status_code=401)
    return user

@app.route('/users/<int:id>/socials', methods=['GET'])
def get_all_socials(id):
    socials = Social.get_all_socials(id)
    if not socials:
        raise APIException('Social media accounts not found', status_code=404)
    return jsonify(socials)

@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['GET'])
def get_social(id_user,id_social):
    social = Social.get_social(id_user,id_social)
    if not social:
        raise APIException('Social media account not found', status_code=404) 
    return jsonify(social)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['GET'])
def get_post(id_user,id_social,id_post):
    post = Post.get_post(new_id_user,new_id_social,new_id_post)
    if not post:
        raise APIException('Post not found', status_code=404) 
    return jsonify(post)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts', methods=['GET'])
def get_all_post(id_user,id_social):
    posts = Post.get_all_post(id_user,id_social)
    if not posts:
        raise APIException('Posts not found', status_code=404)
    return jsonify(posts)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias', methods=['GET'])
def get_all_multimedia(id_user,id_social,id_post):
    multimedias = Multimedia.get_all_multimedia(id_user,id_social,id_post)
    if not multimedias:
        raise APIException('Multimedia not found', status_code=404)
    return jsonify(multimedias)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias/<int:id_multimedia>', methods=['GET'])
def get_multimedia(id_user,id_social,id_post,id_multimedia):
    multimedia = Multimedia.get_multimedia(id_user,id_social,id_post,id_multimedia)
    if not multimedia:
        raise APIException('Multimedia not found', status_code=404)
    return jsonify(multimedia)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
