"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response, redirect, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Social, Post, Multimedia
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import jwt
import datetime
import tweepy


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
        
#         if 'authorization' in request.headers:
#             token = request.headers['authorization']

#         if not token:
#             return jsonify({'message': 'token required'}), 401
        
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.get_user_by_email(data['email'],data['password'])
           
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user,  *args, **kwargs)
#     return decorated

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login', methods=['POST'])
def get_user_by_email():
    body=request.get_json()
    user=User.get_user_by_email(body["email"],body["password"])
    if not user:
      raise APIException('User not found', status_code=404) 
    else:
        access_token = create_access_token(identity=user["username"])
    return jsonify(access_token=access_token), 200

@app.route('/login/twitter')
def login_twitter():
    auth = tweepy.OAuthHandler("ocTqQ5SsxoOppq2jwkZzHbwk7", "g7Upg2lJ3WEjY3EovbSNTBrdly3HriXK2se0fAFd6pLQxabmUn")
    # Redirect user to Twitter to authorize 
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

@app.route('/login/twitter/auth')
def auth_twitter():
    request_token = session['request_token']
    del session['request_token']
    auth = tweepy.OAuthHandler("ocTqQ5SsxoOppq2jwkZzHbwk7", "g7Upg2lJ3WEjY3EovbSNTBrdly3HriXK2se0fAFd6pLQxabmUn")
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)

    return str(api.me())
     
    

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required
def get_user(id):
    user = User.get_user(id)
    if not user:
      raise APIException('User not found', status_code=404)
    else:
      return jsonify(user)

@app.route('/users/<int:id>', methods=['PUT','PATCH'])
@jwt_required
def update_user(id):
    body=request.get_json()
    if User.update_user(id, body) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.update_user(id,body)

@app.route('/users/<int:id>/socials', methods=['GET'])
def get_all_socials(id):
    socials = Social.get_all_socials(id)
    if not socials:
        raise APIException('Social media accounts not found', status_code=404)
    return jsonify(socials)

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    if User.get_user(id) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.delete_user(id)


@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['GET'])
@jwt_required
def get_social(id_user,id_social):
    social = Social.get_social(id_user,id_social)
    if not social:
        raise APIException('Social media account not found', status_code=404)
    return jsonify(social)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['PUT','PATCH'])
def update_post(id_user,id_social,id_post):
    body=request.get_json()
    post = Post.get_post(id_user,id_social,id_post)
    if not post:
        raise APIException('Post not found', status_code=404)
    else:
        return jsonify(post)

@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['PUT','PATCH'])
@jwt_required
def update_social(id_user,id_social):
    body=request.get_json()
    if Social.update_social(id_user,id_social,body) is None:
        raise APIException('Social media account not found', status_code=404) 
    else:
        return jsonify(Social.update_social(id_user,id_social,body))

@app.route('/users/<int:id_user>/socials/<int:id_social>', methods=['DELETE'])
@jwt_required
def delete_social(id_user,id_social):
    if Social.get_social(id_user,id_social) is None:
        raise APIException('Social not found', status_code=404)
    else:
        return Social.delete_social(id_user,id_social)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['GET'])
@jwt_required
def get_post(id_user,id_social,id_post):
    post = Post.get_post(new_id_user,new_id_social,new_id_post)
    if not post:
        raise APIException('Post not found', status_code=404) 
    return jsonify(post)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts', methods=['GET'])
@jwt_required
def get_all_post(id_user,id_social):
    posts = Post.get_all_post(id_user,id_social)
    if not posts:
        raise APIException('Posts not found', status_code=404)
    return jsonify(posts)


@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>', methods=['DELETE'])
@jwt_required
def delete_post(id_user,id_social,id_post):
    if Post.get_post(id_user,id_social,id_post) is None:
        raise APIException('Post not found', status_code=404)
    else:
        return Post.delete_post(id_user,id_social,id_post)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias', methods=['GET'])
@jwt_required
def get_all_multimedia(id_user,id_social,id_post):
    multimedias = Multimedia.get_all_multimedia(id_user,id_social,id_post)
    if not multimedias:
        raise APIException('Multimedia not found', status_code=404)
    return jsonify(multimedias)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias/<int:id_multimedia>', methods=['GET'])
@jwt_required
def get_multimedia(id_user,id_social,id_post,id_multimedia):
    multimedia = Multimedia.get_multimedia(id_user,id_social,id_post,id_multimedia)
    if not multimedia:
        raise APIException('Multimedia not found', status_code=404)
    return jsonify(multimedia)

@app.route('/users/<int:id_user>/socials/<int:id_social>/posts/<int:id_post>/multimedias/<int:id_multimedia>', methods=['DELETE'])
@jwt_required
def delete_multimedia(id_user,id_social,id_post,id_multimedia):
    if Multimedia.get_multimedia(id_user,id_social,id_post,id_multimedia) is None:
        raise APIException('Multimedia not found', status_code=404)
    else:
        return Multimedia.delete_multimedia(id_user,id_social,id_post,id_multimedia)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
