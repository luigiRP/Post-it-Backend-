 #flask
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, redirect, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from utils import APIException, generate_sitemap, validation_username, validation_email, validation_name, validation_password, validation_date
from admin import setup_admin
from models import db, User, Post, Social, Multimedia
import json
import bcrypt
#from models import Person

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400
    user = User.query.filter_by(username = username).first()
    if not user:
        return "User not found", 400
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return f"Welcome back {username}"
    else:
        return "Wrong password"
    




@app.route('/profile', methods=['POST'])
def profile():
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400
    social = Social.query.filter_by(username = username).first()
    if not social:
        return "User not found", 400
    if bcrypt.checkpw(password.encode("utf-8"), social.password.encode("utf-8")):
        return f"Welcome back {username}"
    else:
        return "Wrong password"


@app.route('/users', methods=['POST'])
def add_user():
    data_user = request.get_json()
    valid_username = validation_username(data_user)
    valid_email = validation_email(data_user)
    valid_name = validation_name(data_user)
    valid_password = validation_password(data_user)
    check_new_username = request.json.get("username", None)
    check_new_password = request.json.get("password", None)
    if not check_new_username:
        return "Missing username", 400
    if not check_new_password:
        return "Missing password", 400

    if valid_username == True and valid_email == True and valid_name == True and valid_password == True:
        User.post_user(data_user)
        return "Successful registration", 200
    else:
        return "Error", 303

@app.route('/users/<int:id>', methods=['GET'])
def get_user_id(id):
    if User.get_user(id) is None:
        raise APIException('User not found', status_code=404)
    else:
        return User.get_user(id)

@app.route('/socials', methods=['POST'])
def add_social():
    data_social = request.get_json()
    check_new_username = request.json.get("username", None)
    check_new_password = request.json.get("password", None)
    if not check_new_username:
        return "Missing username", 400
    if not check_new_password:
        return "Missing password", 400
    Social.post_social(data_social)
    return "Successful registration", 200

@app.route('/posts', methods=['POST'])
def add_post():
    posting = request.get_json()
    valid_date = validation_date(posting)
    if valid_date == True:
        Post.post_posts(posting)
        return "Successful registration", 200
    else:
        return "Error", 303
    
@app.route('/multimedias', methods=['POST'])
def add_multimedia():
    data_multimedia = request.get_json()
    Multimedia.post_multimedia(data_multimedia)
    return "Successful registration", 200
    



@app.route("/login")
def loginOAuth():
    #return request.base_url, 200
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace('http://', 'https://') + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace('http://', 'https://'),
        redirect_url=request.base_url.replace('http://', 'https://'),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        picture = userinfo_response.json()["picture"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id, name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("sitemap").replace('http://', 'https://'))


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)