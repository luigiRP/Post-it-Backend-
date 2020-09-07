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
    if User.get_user(id) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.get_user(id)


@app.route('/users/<int:id>', methods=['PUT','PATCH'])
def update_user(id):
    body=request.get_json()
    if User.update_user(id, body) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.update_user(id,body)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    if User.get_user(id) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.delete_user(id)

@app.route('/login', methods=['GET'])
def get_user_by_email():
    body=request.get_json()
    if User.get_user_by_email(body["email"],body["password"]) is "email":
        raise APIException("email doesn't exist", status_code=404)
    elif User.get_user_by_email(body["email"],body["password"]) is "password":
        raise APIException("password for that email doesn't exist", status_code=404)
    else:
        return User.get_user_by_email(body["email"],body["password"])


@app.route('/users/<int:id>/socials', methods=['GET'])
def get_all_socials(id):
    if Social.get_all_socials(id) is None:
        raise APIException('Social media accounts not found', status_code=404)
    else:
        return jsonify(Social.get_all_socials(id))

@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['GET'])
def get_social(id_user,id_social):
    if Social.get_social(id_user,id_social) is None:
        raise APIException('Social media account not found', status_code=404) 
    else:
        return jsonify(Social.get_social(id_user,id_social))

@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['PUT','PATCH'])
def update_social(id_user,id_social):
    body=request.get_json()
    if Social.update_social(id_user,id_social,body) is None:
        raise APIException('Social media account not found', status_code=404) 
    else:
        return jsonify(Social.update_social(id_user,id_social,body))

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['GET'])
def get_post(id_user,id_social,id_post):
    if Post.get_post(id_user,id_social,id_post) is None:
        raise APIException('Post not found', status_code=404) 
    else:
        return jsonify(Post.get_post(id_user,id_social,id_post))

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts', methods=['GET'])
def get_all_post(id_user,id_social):
    if Post.get_all_post(id_user,id_social) is None:
        raise APIException('Posts not found', status_code=404)
    else: 
        return jsonify(Post.get_all_post(id_user,id_social))


@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['PUT','PATCH'])
def update_post(id_user,id_social,id_post):
    body=request.get_json()
    if Post.update_post(id_user,id_social,id_post,body) is None:
        raise APIException('Post not found', status_code=404) 
    else:
        return jsonify(Post.update_post(id_user,id_social,id_post,body))

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias', methods=['GET'])
def get_all_multimedia(id_user,id_social,id_post):
    if Multimedia.get_all_multimedia(id_user,id_social,id_post) is None:
        raise APIException('Multimedia not found', status_code=404)
    else: 
        return jsonify(Multimedia.get_all_multimedia(id_user,id_social,id_post))

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias/<int:id_multimedia>', methods=['GET'])
def get_multimedia(id_user,id_social,id_post,id_multimedia):
    if Multimedia.get_multimedia(id_user,id_social,id_post,id_multimedia) is None:
        raise APIException('Multimedia not found', status_code=404)
    else: 
        return jsonify(Multimedia.get_multimedia(id_user,id_social,id_post,id_multimedia))


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
